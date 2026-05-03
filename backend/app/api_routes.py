from fastapi import APIRouter, HTTPException, Query
from app.services.lichess_service import get_theoretical_moves
from app.services.stockfish_service import evaluate_position
from app.services.youtube_service import search_youtube_videos
from app.utils.chess_utils import validate_fen

router = APIRouter()


@router.get("/api/v1/moves")
def get_moves(fen: str = Query(...)):
    #  validation FEN
    if not validate_fen(fen):
        raise HTTPException(status_code=400, detail="Invalid FEN")

    #  coups théoriques (Lichess)
    try:
        moves = get_theoretical_moves(fen)
    except Exception as e:
        print("Erreur Lichess :", e)
        moves = ["e4", "d4", "Nf3", "c4"]

    #  évaluation Stockfish
    try:
        evaluation = evaluate_position(fen)
    except Exception as e:
        print("Erreur Stockfish :", e)
        evaluation = {"score": 0, "best_move": "e4"}

    #  vidéos YouTube
    try:
        videos = search_youtube_videos("chess opening")
    except Exception as e:
        print("Erreur YouTube :", e)
        videos = []

    #  contexte simple (temporaire)
    context = "Développement des pièces et contrôle du centre"

    return {
        "moves": moves,
        "evaluation": evaluation,
        "context": context,
        "videos": videos
    }