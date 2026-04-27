from stockfish import Stockfish
import os

DOCKER_PATH = "/usr/games/stockfish"

LOCAL_PATH = "C:/Users/selma/Downloads/stockfish-windows-x86-64-avx2/stockfish/stockfish-windows-x86-64-avx2.exe"


def get_stockfish():
    #  Auto-détection environnement
    if os.path.exists(DOCKER_PATH):
        path = DOCKER_PATH
    elif os.path.exists(LOCAL_PATH):
        path = LOCAL_PATH
    else:
        raise FileNotFoundError(" Stockfish introuvable (Docker + Local)")

    return Stockfish(path=path)


def evaluate_position(fen: str):
    try:
        stockfish = get_stockfish()

        stockfish.set_fen_position(fen)
        stockfish.set_depth(15)

        evaluation = stockfish.get_evaluation()

        return {
            "type": evaluation["type"],
            "value": evaluation["value"]
        }

    except Exception as e:
        return {
            "error": str(e)
        }