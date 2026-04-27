from langgraph.graph import StateGraph
from typing import TypedDict

from app.services.lichess_service import get_theoretical_moves
from app.services.stockfish_service import evaluate_position


class AgentState(TypedDict):
    fen: str
    moves: list | None
    evaluation: dict | None
    source: str | None


# 🔹 Node 1: check lichess
def check_lichess(state: AgentState):
    moves = get_theoretical_moves(state["fen"])

    if moves:
        return {
            "moves": moves,
            "source": "lichess"
        }

    return {
        "moves": None
    }


# 🔹 Node 2: fallback stockfish
def check_stockfish(state: AgentState):
    evaluation = evaluate_position(state["fen"])

    return {
        "evaluation": evaluation,
        "source": "stockfish"
    }


# 🔹 Décision
def route(state: AgentState):
    if state.get("moves"):
        return "end"
    return "stockfish"


# 🔥 Build graph
builder = StateGraph(AgentState)

builder.add_node("lichess", check_lichess)
builder.add_node("stockfish", check_stockfish)

builder.set_entry_point("lichess")

builder.add_conditional_edges(
    "lichess",
    route,
    {
        "stockfish": "stockfish",
        "end": "__end__"
    }
)

builder.add_edge("stockfish", "__end__")

graph = builder.compile()