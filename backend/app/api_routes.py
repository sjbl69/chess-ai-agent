from fastapi import APIRouter, HTTPException, Query

from app.services.lichess_service import get_theoretical_moves
from app.services.stockfish_service import evaluate_position
from app.services.youtube_service import search_youtube_videos
from app.services.vector_service import search_similar_positions

from app.utils.chess_utils import validate_fen

router = APIRouter()


# ♟️ 1. Récupérer les coups théoriques (Lichess)
@router.get("/api/v1/moves")
def get_moves(fen: str = Query(...)):
    if not validate_fen(fen):
        raise HTTPException(status_code=400, detail="FEN invalide")

    try:
        moves = get_theoretical_moves(fen)

        if moves is None:
            raise HTTPException(status_code=502, detail="Erreur Lichess")

        return {"moves": moves}

    except Exception as e:
        print("Erreur /moves:", e)
        raise HTTPException(status_code=500, detail="Erreur interne")


# 📊 2. Évaluation Stockfish
@router.get("/api/v1/evaluate")
def evaluate(fen: str = Query(...)):
    if not validate_fen(fen):
        raise HTTPException(status_code=400, detail="FEN invalide")

    try:
        evaluation = evaluate_position(fen)

        if evaluation is None:
            raise HTTPException(status_code=500, detail="Erreur Stockfish")

        return {"evaluation": evaluation}

    except Exception as e:
        print("Erreur /evaluate:", e)
        raise HTTPException(status_code=500, detail="Erreur interne")


# 🔍 3. Vector Search (Milvus / fallback)
@router.get("/vector-search")
def vector_search(query: str = Query(...)):
    try:
        results = search_similar_positions(query)

        if results is None:
            raise HTTPException(status_code=500, detail="Erreur vector search")

        return {"results": results}

    except Exception as e:
        print("Erreur /vector-search:", e)
        raise HTTPException(status_code=500, detail="Erreur interne")


# 🎥 4. Vidéos YouTube par ouverture
@router.get("/api/v1/videos/{opening}")
def get_videos(opening: str):
    try:
        videos = search_youtube_videos(opening)

        if not videos:
            raise HTTPException(status_code=404, detail="Aucune vidéo trouvée")

        return {"videos": videos}

    except Exception as e:
        print("Erreur /videos:", e)
        raise HTTPException(status_code=500, detail="Erreur interne")