import sqlite3
from collections import Counter
from db import DB_PATH

def get_mate_squares(opening, mated_side):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT mate_square FROM games
        WHERE opening = ? AND mated_side = ?
    """, (opening, mated_side))

    rows = cursor.fetchall()
    conn.close()
    squares = [row[0] for row in rows]
    return Counter(squares)


def get_opening_stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT opening, COUNT(*) as total_games,
            AVG(move_count) as avg_moves
        FROM games
        GROUP BY opening
        ORDER BY total_games DESC
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows


def get_mating_pieces(opening):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT mating_piece, COUNT(*) as total
        FROM games
        WHERE opening = ?
        GROUP BY mating_piece
        ORDER BY total DESC
    """, (opening,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_opening_summary(opening):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT mated_side, mate_square, COUNT(*) as total
        FROM games
        WHERE opening = ?
        GROUP BY mated_side, mate_square
        ORDER BY mated_side, total DESC
    """, (opening,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_mating_pieces_by_rating(opening, min_elo, max_elo):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT mating_piece, COUNT(*) as total
        FROM games
        WHERE opening = ?
          AND white_elo BETWEEN ? AND ?
          AND black_elo BETWEEN ? AND ?
        GROUP BY mating_piece
        ORDER BY total DESC
    """, (opening, min_elo, max_elo, min_elo, max_elo))
    rows = cursor.fetchall()
    conn.close()
    return rows