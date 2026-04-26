from fastapi import APIRouter
from pydantic import BaseModel
from stockfish import Stockfish

router = APIRouter()

class PositionRequest(BaseModel):
    fen: str

stockfish = Stockfish(path="/usr/games/stockfish")

@router.post("/evaluate")
def evaluate_position(request: PositionRequest):
    stockfish.set_fen_position(request.fen)
    
    best_move = stockfish.get_best_move()
    evaluation = stockfish.get_evaluation()

    return {
        "best_move": best_move,
        "evaluation": evaluation
    }