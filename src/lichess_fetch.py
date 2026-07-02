import requests
import chess.pgn
import io
from collections import defaultdict
from pgn_parser import parse_game

LICHESS_API_URL = "https://lichess.org/api/games/user/{username}"

def fetch_user_mate_games(username, max_games=500):
    """
    Fetches recent games for a Lichess user and returns only the ones
    where that user was checkmated, parsed via the existing parse_game().
    """
    params = {
        "max": max_games,
        "opening": "true",
        "clocks": "false",
        "evals": "false",
    }
    headers = {"Accept": "application/x-chess-pgn"}

    response = requests.get(
        LICHESS_API_URL.format(username=username),
        params=params,
        headers=headers,
        stream=True,
        timeout=30,
    )
    response.raise_for_status()

    pgn_text = response.text
    pgn_stream = io.StringIO(pgn_text)

    results = []
    total_games_checked = 0
    while True:
        game = chess.pgn.read_game(pgn_stream)
        if game is None:
            break
        total_games_checked += 1

        parsed = parse_game(game)
        if parsed is None:
            continue  # not a checkmate game, skip

        # Only keep it if THIS user was the one who got mated
        white_name = game.headers.get("White", "").lower()
        black_name = game.headers.get("Black", "").lower()
        target = username.lower()

        if parsed["mated_side"] == "White" and white_name == target:
            results.append(parsed)
        elif parsed["mated_side"] == "Black" and black_name == target:
            results.append(parsed)

    return results, total_games_checked


def aggregate_personal_mate_squares(parsed_games, total_games_checked):
    """
    Takes the list of parsed checkmate games (from fetch_user_mate_games)
    and rolls them up into the same {"white": {...}, "black": {...}} shape
    that the existing heatmap frontend (drawBoard in script.js) expects.

    Note: for a personal lookup, "white" counts are games where the user
    got mated while playing White, and "black" counts are games where the
    user got mated while playing Black -- NOT split by opponent color.
    """
    white_counts = defaultdict(int)
    black_counts = defaultdict(int)

    for game in parsed_games:
        square = game["mate_square"]
        if game["mated_side"] == "White":
            white_counts[square] += 1
        else:
            black_counts[square] += 1

    return {
        "white": dict(white_counts),
        "black": dict(black_counts),
        "total_games": len(parsed_games),
        "total_games_checked": total_games_checked,
    }