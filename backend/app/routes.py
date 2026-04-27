from fastapi import APIRouter, HTTPException, Query
from app.services.lichess_service import get_theoretical_moves
from app.services.stockfish_service import evaluate_position
from app.utils.chess_utils import validate_fen
from app.agent import graph  

router = APIRouter()


@router.get("/api/v1/moves")
def get_moves(fen: str = Query(...)):
    board = validate_fen(fen)
    if not board:
        raise HTTPException(status_code=400, detail="FEN invalide")

    try:
        moves = get_theoretical_moves(fen)
    except Exception:
        raise HTTPException(status_code=502, detail="Erreur API Lichess")

    if not moves:
        raise HTTPException(status_code=404, detail="Aucun coup théorique trouvé")

    return {
        "source": "lichess",
        "fen": fen,
        "moves": moves
    }


@router.get("/api/v1/evaluate")
def evaluate(fen: str = Query(...)):
    board = validate_fen(fen)
    if not board:
        raise HTTPException(status_code=400, detail="FEN invalide")

    try:
        evaluation = evaluate_position(fen)
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur Stockfish")

    if not evaluation:
        raise HTTPException(status_code=500, detail="Impossible d’évaluer la position")

    return {
        "source": "stockfish",
        "fen": fen,
        "evaluation": evaluation
    }


#  VERSION LANGGRAPH 
@router.get("/api/v1/analyze")
def analyze_position(fen: str = Query(...)):
    board = validate_fen(fen)
    if not board:
        raise HTTPException(status_code=400, detail="FEN invalide")

    try:
        result = graph.invoke({
            "fen": fen,
            "moves": None,
            "evaluation": None,
            "source": None
        })
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur agent IA")

    return result