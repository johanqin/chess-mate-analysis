import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "chess.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            opening TEXT,
            eco TEXT,
            result TEXT,
            mated_side TEXT,
            mate_square TEXT,
            move_count INTEGER,
            white_elo INTEGER,
            black_elo INTEGER,
            time_control TEXT,
            mating_piece TEXT,
            mate_type TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_games(parsed_games):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    count = 0
    for game in parsed_games:
        cursor.execute("""
            INSERT INTO games (
                opening, eco, result, mated_side, mate_square,
                move_count, white_elo, black_elo, time_control,
                mating_piece, mate_type
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            game["opening"],
            game["eco"],
            game["result"],
            game["mated_side"],
            game["mate_square"],
            game["move_count"],
            game["white_elo"],
            game["black_elo"],
            game["time_control"],
            game["mating_piece"],
            game["mate_type"],
        ))
        count += 1
        if count % 1000 == 0:
            print(f"Saved {count} checkmate games so far...")
    conn.commit()
    conn.close()
    print(f"Finished! Total checkmate games saved: {count}")