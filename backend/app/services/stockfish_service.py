def evaluate_position(fen: str):
    try:
        stockfish.set_fen_position(fen)
        return stockfish.get_evaluation()
    except Exception:
        return {"score": 0}