from fastapi import APIRouter, HTTPException, Query
from app.services.lichess_service import get_theoretical_moves
from app.services.stockfish_service import evaluate_position
from app.utils.chess_utils import validate_fen
from app.agent import chess_agent

router = APIRouter()


#  1. Endpoint MOVES (Lichess)
@router.get("/api/v1/moves")
def get_moves(fen: str = Query(..., description="FEN position")):
    board = validate_fen(fen)
    if not board:
        raise HTTPException(status_code=400, detail="FEN invalide")

    try:
        moves = get_theoretical_moves(fen)
    except Exception:
        raise HTTPException(status_code=503, detail="Lichess unavailable")

    return {
        "source": "lichess",
        "fen": fen,
        "moves": moves or []
    }


#  2. Endpoint EVALUATE (Stockfish)
@router.get("/api/v1/evaluate")
def evaluate(fen: str = Query(..., description="FEN position")):
    board = validate_fen(fen)
    if not board:
        raise HTTPException(status_code=400, detail="FEN invalide")

    try:
        evaluation = evaluate_position(fen)
    except Exception:
        raise HTTPException(status_code=500, detail="Stockfish error")

    return {
        "source": "stockfish",
        "fen": fen,
        "evaluation": evaluation
    }


#  3. Endpoint ANALYZE (Agent)
@router.get("/api/v1/analyze")
def analyze_position(fen: str = Query(..., description="FEN position")):
    board = validate_fen(fen)
    if not board:
        raise HTTPException(status_code=400, detail="FEN invalide")

    try:
        moves = get_theoretical_moves(fen)
    except Exception:
        moves = None

    try:
        evaluation = evaluate_position(fen)
    except Exception:
        evaluation = None

    decision = chess_agent(fen, moves, evaluation)

    return {
        "fen": fen,
        "result": decision
    }