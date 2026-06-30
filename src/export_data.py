import json
from analyze import get_opening_stats, get_opening_summary

def export_all_openings(min_games=500):
    stats = get_opening_stats()
    openings = [row[0] for row in stats if row[1] >= min_games]

    data = {}
    for opening in openings:
        rows = get_opening_summary(opening)
        white = {}
        black = {}
        for mated_side, square, count in rows:
            if mated_side == "White":
                white[square] = count
            else:
                black[square] = count
        data[opening] = {"white": white, "black": black}

    with open("src/static/mate_data.json", "w") as f:
        json.dump(data, f)

    print(f"Exported {len(openings)} openings to mate_data.json")

if __name__ == "__main__":
    export_all_openings()