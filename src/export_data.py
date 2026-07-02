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

# Base time thresholds (seconds) follow Lichess's own speed categories.
# Classical and correspondence are intentionally excluded as filter options —
# sample sizes get too thin once crossed with opening x rating band.
SPEED_BUCKETS = [
    ("all", None),
    ("bullet", (0, 180)),
    ("blitz", (180, 480)),
    ("rapid", (480, 1500)),
]

# SQL fragment that buckets the raw time_control string ("600+0") into a
# speed category. Returns NULL for classical/correspondence/malformed values
# so they're naturally excluded from any bucket other than "all".
SPEED_CASE_SQL = """
    CASE
        WHEN time_control IS NULL OR time_control = '-' OR INSTR(time_control, '+') = 0 THEN NULL
        WHEN CAST(SUBSTR(time_control, 1, INSTR(time_control, '+') - 1) AS INTEGER) < 180 THEN 'bullet'
        WHEN CAST(SUBSTR(time_control, 1, INSTR(time_control, '+') - 1) AS INTEGER) < 480 THEN 'blitz'
        WHEN CAST(SUBSTR(time_control, 1, INSTR(time_control, '+') - 1) AS INTEGER) < 1500 THEN 'rapid'
        ELSE NULL
    END
"""

def clean_name(opening):
    opening = re.sub(r'\s*#\d+$', '', opening)
    opening = opening.split(':')[0].strip()
    opening = opening.split(',')[0].strip()
    opening = ALIASES.get(opening, opening)
    return opening

def get_opening_summary_by_rating_and_speed(opening, min_elo, max_elo, speed_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    where_clauses = ["opening = ?"]
    params = [opening]

    if not (min_elo == 0 and max_elo == 3000):
        where_clauses.append("white_elo BETWEEN ? AND ?")
        where_clauses.append("black_elo BETWEEN ? AND ?")
        params.extend([min_elo, max_elo, min_elo, max_elo])

    if speed_name != "all":
        where_clauses.append(f"({SPEED_CASE_SQL}) = ?")
        params.append(speed_name)

    query = f"""
        SELECT mated_side, mate_square, COUNT(*) as total
        FROM games
        WHERE {' AND '.join(where_clauses)}
        GROUP BY mated_side, mate_square
        ORDER BY mated_side, total DESC
    """

    cursor.execute(query, params)
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

        for speed_name, _ in SPEED_BUCKETS:
            data[clean_opening][speed_name] = {}

            for band_name, min_elo, max_elo in RATING_BANDS:
                white_counts = defaultdict(int)
                black_counts = defaultdict(int)

                for raw_opening in raw_openings:
                    rows = get_opening_summary_by_rating_and_speed(
                        raw_opening, min_elo, max_elo, speed_name
                    )
                    for mated_side, square, count in rows:
                        if mated_side == "White":
                            white_counts[square] += count
                        else:
                            black_counts[square] += count

                data[clean_opening][speed_name][band_name] = {
                    "white": dict(white_counts),
                    "black": dict(black_counts)
                }

        print(f"Exported: {clean_opening}")

    with open("src/static/mate_data.json", "w") as f:
        json.dump(data, f)

    print(
        f"\nDone! Exported {len(data)} openings with "
        f"{len(SPEED_BUCKETS)} speed buckets x {len(RATING_BANDS)} rating bands each."
    )

if __name__ == "__main__":
    export_all_openings()