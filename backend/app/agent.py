from langgraph.graph import StateGraph
from typing import TypedDict

from app.services.lichess_service import get_theoretical_moves
from app.services.stockfish_service import evaluate_position
from app.services.vector_service import search_opening
from app.services.youtube_service import search_youtube_videos


class AgentState(TypedDict):
    fen: str
    moves: list | None
    evaluation: dict | None
    source: str | None
    opening: str | None
    videos: list | None


#  Node 1: check lichess
def check_lichess(state: AgentState):
    moves = get_theoretical_moves(state["fen"])

    return {
        **state,
        "moves": moves if moves else None,
        "source": "lichess" if moves else state.get("source")
    }


#  Node 2: fallback stockfish
def check_stockfish(state: AgentState):
    evaluation = evaluate_position(state["fen"])

    return {
        **state,
        "evaluation": evaluation,
        "source": "stockfish"
    }


#  Node 3: detect opening
def detect_opening(state: AgentState):
    try:
        result = search_opening(state["fen"])
        opening = result.get("opening")
    except Exception:
        opening = None

    return {
        **state,
        "opening": opening
    }


#  Node 4: youtube videos
def youtube_node(state: AgentState):
    opening = state.get("opening")

    if not opening:
        return {**state, "videos": []}

    try:
        videos = search_youtube_videos(opening)
    except Exception:
        videos = []

    return {
        **state,
        "videos": videos
    }


#  Décision
def route(state: AgentState):
    if state.get("moves"):
        return "opening"
    return "stockfish"


#  Build graph
builder = StateGraph(AgentState)

builder.add_node("lichess", check_lichess)
builder.add_node("stockfish", check_stockfish)
builder.add_node("opening", detect_opening)
builder.add_node("youtube", youtube_node)

builder.set_entry_point("lichess")


builder.add_conditional_edges(
    "lichess",
    route,
    {
        "stockfish": "stockfish",
        "opening": "opening"
    }
)

builder.add_edge("stockfish", "opening")
builder.add_edge("opening", "youtube")
builder.add_edge("youtube", "__end__")

graph = builder.compile()