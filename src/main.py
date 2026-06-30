import sys
from pgn_parser import stream_games, stream_games_zst
from db import init_db, save_games

if __name__ == "__main__":
    path = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else None

    print(f"Initializing database...")
    init_db()

    print(f"Processing games from {path}...")
    if path.endswith(".zst"):
        games = stream_games_zst(path, limit=limit)
    else:
        games = stream_games(path)

    save_games(games)
    print("Done!")