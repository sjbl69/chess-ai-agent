from fastapi import APIRouter, Query, HTTPException
import chess

from app.services.vector_service import search_opening
from app.services.stockfish_service import evaluate_position

router = APIRouter()


# ==============================
# PARSE USER INPUT → FEN
# ==============================
def parse_to_fen(user_input: str) -> str:
    # 1. Start position
    if user_input == "startpos":
        return chess.Board().fen()

    # 2. Try direct FEN
    try:
        board = chess.Board(user_input)
        return board.fen()
    except:
        pass

    # 3. Try SAN moves (e4 e5 Nf3)
    board = chess.Board()
    try:
        for move in user_input.split():
            board.push_san(move)
        return board.fen()
    except:
        raise HTTPException(status_code=400, detail="Invalid input")


# ==============================
# API ENDPOINT
# ==============================
@router.get("/api/v1/moves")
def get_moves(fen: str = Query(...)):
    try:
        # 1. Convert input → FEN
        fen_clean = parse_to_fen(fen)

        # 2. Vector search (openings)
        opening_result = search_opening(fen)

        # 3. Stockfish evaluation (SAFE)
        evaluation = {"score": 0}
        try:
            evaluation = evaluate_position(fen_clean)
        except Exception as e:
            print("Stockfish error:", e)

        # 4. Normalize openings
        openings = (
            opening_result.get("moves")
            or opening_result.get("openings")
            or []
        )

        # 5. Response
        return {
            "source": opening_result.get("source", "unknown"),
            "openings": openings,
            "score": evaluation.get("score", 0),
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        print("API ERROR:", e)
        return {
            "source": "error",
            "openings": [],
            "score": 0,
            "error": str(e),
        }