from fastapi import APIRouter, Query, HTTPException
import chess

from app.services.vector_service import search_opening
from app.services.stockfish_service import evaluate_position
from app.services.youtube_service import search_youtube_videos

router = APIRouter()


# PARSE USER INPUT → FEN

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


# ENDPOINT 1 — CHESS MOVES

@router.get("/api/v1/moves")
def get_moves(fen: str = Query(...)):
    try:
        # Convert input → FEN
        fen_clean = parse_to_fen(fen)

        # Vector search (openings)
        opening_result = search_opening(fen)

        # Stockfish evaluation (SAFE)
        evaluation = {"score": 0}
        try:
            evaluation = evaluate_position(fen_clean)
        except Exception as e:
            print("Stockfish error:", e)

        # Normalize openings
        openings = (
            opening_result.get("moves")
            or opening_result.get("openings")
            or []
        )

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


# ENDPOINT 2 — VECTOR SEARCH (étape 3)

@router.get("/vector-search")
def vector_search(query: str = Query(...)):
    try:
        result = search_opening(query)

        return {
            "source": result.get("source", "unknown"),
            "results": result.get("moves") or result.get("openings") or []
        }

    except Exception as e:
        return {
            "source": "error",
            "results": [],
            "error": str(e)
        }


# ENDPOINT 3 — YOUTUBE VIDEOS (étape 4)

@router.get("/api/v1/videos/{opening}")
def get_videos(opening: str):
    try:
        videos = search_youtube_videos(opening)

        return {
            "opening": opening,
            "videos": videos
        }

    except Exception as e:
        return {
            "opening": opening,
            "videos": [],
            "error": str(e)
        }