import chess.pgn
import chess
import zstandard as zstd
import io

def parse_game(game):
    headers = game.headers
    result = headers.get("Result", "*")
    opening = headers.get("Opening", "Unknown")
    eco = headers.get("ECO", "???")
    white_elo = headers.get("WhiteElo", None)
    black_elo = headers.get("BlackElo", None)
    time_control = headers.get("TimeControl", None)
    board = game.end().board()
    if not board.is_checkmate():
        return None
    mated_side = "Black" if board.turn == chess.BLACK else "White"
    mated_king_color = chess.BLACK if mated_side == "Black" else chess.WHITE
    king_square = board.king(mated_king_color)
    mate_square = chess.square_name(king_square)
    last_move = game.end().move
    mating_piece = board.piece_at(last_move.to_square)
    mating_piece_type = mating_piece.symbol() if mating_piece else None
    move_count = game.end().ply() // 2
    return {
        "opening": opening,
        "eco": eco,
        "result": result,
        "mated_side": mated_side,
        "mate_square": mate_square,
        "move_count": move_count,
        "white_elo": white_elo,
        "black_elo": black_elo,
        "time_control": time_control,
        "mating_piece": mating_piece_type,
        "mate_type": None,
    }


def stream_games(pgn_path):
    with open(pgn_path, encoding="utf-8", errors="ignore") as f:
        while True:
            game = chess.pgn.read_game(f)
            if game is None:
                break
            parsed = parse_game(game)
            if parsed is not None:
                yield parsed


def stream_games_zst(zst_path, limit=None):
    dctx = zstd.ZstdDecompressor()
    with open(zst_path, "rb") as fh:
        with dctx.stream_reader(fh) as reader:
            text_stream = io.TextIOWrapper(reader, encoding="utf-8")
            count = 0
            while True:
                game = chess.pgn.read_game(text_stream)
                if game is None:
                    break
                parsed = parse_game(game)
                if parsed is not None:
                    yield parsed
                    count += 1
                    if limit and count >= limit:
                        break