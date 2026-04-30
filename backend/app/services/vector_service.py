from sentence_transformers import SentenceTransformer
import numpy as np

from pymilvus import connections, Collection

model = SentenceTransformer("all-MiniLM-L6-v2")

# connexion Milvus
try:
    connections.connect(host="milvus", port="19530")
    collection = Collection("chess_openings")
    collection.load()
    MILVUS_AVAILABLE = True
    print("Milvus connecté")
except Exception as e:
    print("Milvus non dispo:", e)
    MILVUS_AVAILABLE = False


# fallback local
OPENINGS = [
    "King's Pawn Opening e4",
    "Queen's Gambit d4 c4",
    "Sicilian Defense c5",
    "French Defense e6",
    "Caro-Kann Defense c6"
]

opening_embeddings = model.encode(OPENINGS)


def search_opening(query: str):
    try:
        query_embedding = model.encode([query])[0]

        # CAS MILVUS
        if MILVUS_AVAILABLE:
            results = collection.search(
                data=[query_embedding.tolist()],
                anns_field="embedding",
                param={"metric_type": "COSINE", "params": {"nprobe": 10}},
                limit=3,
                output_fields=["name"]  # IMPORTANT
            )

            openings = []
            for hits in results:
                for hit in hits:
                    openings.append(hit.entity.get("name"))

            if openings:
                return {
                    "source": "milvus",
                    "openings": openings
                }

        # FALLBACK LOCAL
        similarities = np.dot(opening_embeddings, query_embedding)
        best_idx = int(np.argmax(similarities))

        return {
            "source": "local",
            "opening": OPENINGS[best_idx],
            "score": float(similarities[best_idx]),
        }

    except Exception as e:
        return {"error": str(e)}