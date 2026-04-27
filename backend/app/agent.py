def chess_agent(fen: str, moves, evaluation):
    if moves:
        return {
            "decision": "play_theory",
            "moves": moves
        }

    return {
        "decision": "use_stockfish",
        "evaluation": evaluation
    }