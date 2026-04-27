import chess

def validate_fen(fen: str):
    try:
        board = chess.Board(fen)
        return board
    except ValueError:
        return None