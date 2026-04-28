from sentence_transformers import SentenceTransformer
import numpy as np

# Modèle d'embedding
model = SentenceTransformer("all-MiniLM-L6-v2")

# Mini dataset d'ouvertures (fallback sans Milvus)
OPENINGS = [
    {"name": "Sicilian Defense", "description": "e4 c5"},
    {"name": "French Defense", "description": "e4 e6"},
    {"name": "Caro-Kann Defense", "description": "e4 c6"},
    {"name": "Ruy Lopez", "description": "e4 e5 Nf3 Nc6 Bb5"},
    {"name": "Italian Game", "description": "e4 e5 Nf3 Nc6 Bc4"},
    {"name": "Queen's Gambit", "description": "d4 d5 c4"},
]

# Pré-calcul des embeddings
opening_embeddings = model.encode(
    [o["name"] + " " + o["description"] for o in OPENINGS]
)


def search_opening(query: str):
    try:
        query_embedding = model.encode([query])[0]

        # Calcul similarité cosinus
        similarities = np.dot(opening_embeddings, query_embedding)

        best_idx = int(np.argmax(similarities))

        return {
            "opening": OPENINGS[best_idx]["name"],
            "description": OPENINGS[best_idx]["description"],
            "score": float(similarities[best_idx]),
        }

    except Exception as e:
        return {"error": str(e)}