from fastapi import APIRouter, HTTPException, Query

from app.services.lichess_service import get_theoretical_moves
from app.services.stockfish_service import evaluate_position
from app.utils.chess_utils import validate_fen

router = APIRouter()


#  1. COUPS THÉORIQUES (Lichess)
@router.get("/api/v1/moves")
def get_moves(fen: str = Query(..., description="FEN position")):
    
    board = validate_fen(fen)
    if not board:
        raise HTTPException(status_code=400, detail="FEN invalide")

    moves = get_theoretical_moves(fen)

    return {
        "source": "lichess",
        "fen": fen,
        "moves": moves
    }


#  2. ÉVALUATION (Stockfish)
@router.get("/api/v1/evaluate")
def evaluate(fen: str = Query(..., description="FEN position")):
    
    board = validate_fen(fen)
    if not board:
        raise HTTPException(status_code=400, detail="FEN invalide")

    evaluation = evaluate_position(fen)

    return {
        "source": "stockfish",
        "fen": fen,
        "evaluation": evaluation
    }


# AGENT INTELLIGENT
@router.get("/api/v1/analyze")
def analyze_position(fen: str = Query(..., description="FEN position")):
    
    board = validate_fen(fen)
    if not board:
        raise HTTPException(status_code=400, detail="FEN invalide")

    # 1️ Lichess
    moves = get_theoretical_moves(fen)

    if moves:
        return {
            "source": "lichess",
            "fen": fen,
            "moves": moves
        }

    # 2️ Stockfish fallback
    evaluation = evaluate_position(fen)

    return {
        "source": "stockfish",
        "fen": fen,
        "evaluation": evaluation
    }