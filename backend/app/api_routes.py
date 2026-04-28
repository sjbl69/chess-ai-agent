from fastapi import APIRouter, HTTPException, Query

from app.services.lichess_service import get_theoretical_moves
from app.services.stockfish_service import evaluate_position
from app.utils.chess_utils import validate_fen
from app.services.vector_service import search_opening
from app.services.youtube_service import search_youtube_videos
from app.agent import graph

router = APIRouter()


# 1. Moves
@router.get("/api/v1/moves")
def get_moves(fen: str = Query(...)):
    if not validate_fen(fen):
        raise HTTPException(status_code=400, detail="FEN invalide")

    try:
        moves = get_theoretical_moves(fen)
    except Exception:
        raise HTTPException(status_code=502, detail="Erreur API Lichess")

    if not moves:
        raise HTTPException(status_code=404, detail="Aucun coup théorique")

    return {"moves": moves}


# 2. Stockfish
@router.get("/api/v1/evaluate")
def evaluate(fen: str = Query(...)):
    if not validate_fen(fen):
        raise HTTPException(status_code=400, detail="FEN invalide")

    evaluation = evaluate_position(fen)

    return {"evaluation": evaluation}


# 3. Vector search
@router.get("/api/v1/vector-search")
def vector_search(query: str = Query(...)):
    return search_opening(query)


# 4. YouTube
@router.get("/api/v1/videos/{opening}")
def get_videos(opening: str):
    videos = search_youtube_videos(opening)

    if not videos:
        raise HTTPException(status_code=404, detail="Aucune vidéo trouvée")

    return {"videos": videos}


# 5. Analyse complète (agent)
@router.get("/api/v1/analyze")
def analyze(fen: str = Query(...)):
    if not validate_fen(fen):
        raise HTTPException(status_code=400, detail="FEN invalide")

    result = graph.invoke({
        "fen": fen,
        "moves": None,
        "evaluation": None,
        "source": None,
        "opening": None,
        "videos": None
    })

    return {
        "fen": fen,
        "source": result.get("source"),
        "moves": result.get("moves"),
        "evaluation": result.get("evaluation"),
        "opening": result.get("opening"),
        "videos": result.get("videos")
    }