import json
import re
from analyze import get_opening_stats, get_opening_summary
from collections import defaultdict

def clean_name(opening):
    opening = re.sub(r'\s*#\d+$', '', opening)
    opening = opening.split(':')[0].strip()
    opening = opening.split(',')[0].strip()
    return opening

def export_all_openings(min_games=500):
    stats = get_opening_stats()
    openings = [row[0] for row in stats if row[1] >= min_games]

    data = defaultdict(lambda: {"white": defaultdict(int), "black": defaultdict(int)})

    for opening in openings:
        clean = clean_name(opening)
        rows = get_opening_summary(opening)
        for mated_side, square, count in rows:
            key = "white" if mated_side == "White" else "black"
            data[clean][key][square] += count

    final_data = {
        opening: {"white": dict(sides["white"]), "black": dict(sides["black"])}
        for opening, sides in data.items()
    }

    with open("src/static/mate_data.json", "w") as f:
        json.dump(final_data, f)

    print(f"Exported {len(final_data)} cleaned openings to mate_data.json")

if __name__ == "__main__":
    export_all_openings()