from stockfish import Stockfish


def evaluate_position(fen: str):
    try:
        stockfish = Stockfish(path="/usr/games/stockfish")

        stockfish.set_fen_position(fen)
        evaluation = stockfish.get_evaluation()

        return evaluation

    except Exception as e:
        print("Erreur Stockfish:", e)
        return None