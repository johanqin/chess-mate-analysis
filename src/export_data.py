import json
import re
import sqlite3
from collections import defaultdict
from analyze import get_opening_stats, get_opening_summary
from db import DB_PATH

ALIASES = {
    "Danish Gambit Accepted": "Danish Gambit",
    "Englund Gambit": "Englund Gambit Complex",
    "Englund Gambit Complex Declined": "Englund Gambit Complex",
    "Englund Gambit Declined": "Englund Gambit Complex",
    "Gedult's Opening": "Barnes Opening",
    "King's Pawn Game": "King's Pawn",
    "King's Pawn Opening": "King's Pawn",
    "Latvian Gambit Accepted": "Latvian Gambit",
    "Nimzowitsch-Larsen Attack": "Nimzo-Larsen Attack",
    "Petrov's Defense": "Petrov",
    "Queen's Gambit Refused": "Queen's Gambit Declined",
    "Queen's Pawn Game": "Queen's Pawn",
    "Robatsch (Modern) Defense": "Modern Defense",
    "Robatsch Defense": "Modern Defense",
}

RATING_BANDS = [
    ("all", 0, 3000),
    ("beginner", 800, 1200),
    ("intermediate", 1200, 1600),
    ("advanced", 1600, 2000),
    ("expert", 2000, 2400),
]

def clean_name(opening):
    opening = re.sub(r'\s*#\d+$', '', opening)
    opening = opening.split(':')[0].strip()
    opening = opening.split(',')[0].strip()
    opening = ALIASES.get(opening, opening)
    return opening

def get_opening_summary_by_rating(opening, min_elo, max_elo):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if min_elo == 0 and max_elo == 3000:
        cursor.execute("""
            SELECT mated_side, mate_square, COUNT(*) as total
            FROM games
            WHERE opening = ?
            GROUP BY mated_side, mate_square
            ORDER BY mated_side, total DESC
        """, (opening,))
    else:
        cursor.execute("""
            SELECT mated_side, mate_square, COUNT(*) as total
            FROM games
            WHERE opening = ?
              AND white_elo BETWEEN ? AND ?
              AND black_elo BETWEEN ? AND ?
            GROUP BY mated_side, mate_square
            ORDER BY mated_side, total DESC
        """, (opening, min_elo, max_elo, min_elo, max_elo))
    rows = cursor.fetchall()
    conn.close()
    return rows

def export_all_openings(min_games=500):
    stats = get_opening_stats()
    
    # Build cleaned opening map
    opening_map = defaultdict(list)
    for row in stats:
        if row[1] >= min_games:
            clean = clean_name(row[0])
            opening_map[clean].append(row[0])

    data = {}
    
    for clean_opening, raw_openings in opening_map.items():
        data[clean_opening] = {}
        
        for band_name, min_elo, max_elo in RATING_BANDS:
            white_counts = defaultdict(int)
            black_counts = defaultdict(int)
            
            for raw_opening in raw_openings:
                rows = get_opening_summary_by_rating(raw_opening, min_elo, max_elo)
                for mated_side, square, count in rows:
                    if mated_side == "White":
                        white_counts[square] += count
                    else:
                        black_counts[square] += count
            
            data[clean_opening][band_name] = {
                "white": dict(white_counts),
                "black": dict(black_counts)
            }
        
        print(f"Exported: {clean_opening}")

    with open("src/static/mate_data.json", "w") as f:
        json.dump(data, f)

    print(f"\nDone! Exported {len(data)} openings with {len(RATING_BANDS)} rating bands each.")

if __name__ == "__main__":
    export_all_openings()