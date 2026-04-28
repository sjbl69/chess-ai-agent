from fastapi import APIRouter, HTTPException, Query

from app.services.lichess_service import get_theoretical_moves
from app.services.stockfish_service import evaluate_position
from app.utils.chess_utils import validate_fen
from app.services.vector_service import search_opening
from app.agent import graph  

router = APIRouter()


# ♟️ 1. Coups théoriques (Lichess)
@router.get("/api/v1/moves")
def get_moves(fen: str = Query(...)):
    if not validate_fen(fen):
        raise HTTPException(status_code=400, detail="FEN invalide")

    try:
        moves = get_theoretical_moves(fen)
    except Exception:
        raise HTTPException(status_code=502, detail="Erreur API Lichess")

    if not moves:
        raise HTTPException(status_code=404, detail="Aucun coup théorique trouvé")

    return {"source": "lichess", "moves": moves}


#  2. Évaluation Stockfish
@router.get("/api/v1/evaluate")
def evaluate(fen: str = Query(...)):
    if not validate_fen(fen):
        raise HTTPException(status_code=400, detail="FEN invalide")

    try:
        evaluation = evaluate_position(fen)
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur Stockfish")

    if not evaluation:
        raise HTTPException(status_code=500, detail="Impossible d’évaluer la position")

    return {"source": "stockfish", "evaluation": evaluation}


#  3. Vector Search (SANS Milvus - fallback local)
@router.get("/api/v1/vector-search")
def vector_search(query: str = Query(...)):
    try:
        result = search_opening(query)
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur vector search")

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    return result


#  4. Analyse complète (LangGraph agent)
@router.get("/api/v1/analyze")
def analyze(fen: str = Query(...)):
    if not validate_fen(fen):
        raise HTTPException(status_code=400, detail="FEN invalide")

    try:
        result = graph.invoke({
            "fen": fen,
            "moves": None,
            "evaluation": None,
            "source": None
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur agent IA")

    return {
        "fen": fen,
        "source": result.get("source"),
        "moves": result.get("moves"),
        "evaluation": result.get("evaluation")
    }