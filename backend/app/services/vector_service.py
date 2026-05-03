"""
Vector Search Service (Milvus + fallback)

- Utilise la collection 'chess_openings'
- Fait une vraie recherche vectorielle avec collection.search
- Utilise des embeddings si le modèle est dispo
- Fallback simulé si Milvus ou modèle indisponible
"""

from typing import List, Dict

# Milvus 
try:
    from pymilvus import connections, Collection
    MILVUS_AVAILABLE = True
except Exception:
    MILVUS_AVAILABLE = False

# Embedding 
try:
    from sentence_transformers import SentenceTransformer
    _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    EMBEDDING_AVAILABLE = True
except Exception:
    _model = None
    EMBEDDING_AVAILABLE = False


def _fallback(query: str) -> List[Dict]:
    """Fallback simulé (ne casse jamais l’API)."""
    q = query.lower()
    if "sicilian" in q:
        return [
            {"id": 1, "opening": "Sicilian Defense", "score": 0.95},
            {"id": 2, "opening": "Najdorf Variation", "score": 0.92},
        ]
    if "french" in q:
        return [
            {"id": 3, "opening": "French Defense", "score": 0.96},
            {"id": 4, "opening": "Advance Variation", "score": 0.90},
        ]
    return [{"id": 0, "opening": "Unknown Opening", "score": 0.80}]


def search_similar_positions(query: str) -> List[Dict]:
    """
    Recherche vectorielle sur Milvus (collection: chess_openings).
    """
    if not query or not isinstance(query, str):
        return []

    # Si Milvus ou embeddings indisponibles → fallback
    if not (MILVUS_AVAILABLE and EMBEDDING_AVAILABLE):
        return _fallback(query)

    try:
        # Connexion Milvus (adapter host/port si besoin)
        connections.connect(host="milvus", port="19530")

        #  IMPORTANT : même nom que dans load_openings.py
        collection = Collection("chess_openings")

        # Encoder la requête en vecteur
        query_vector = _model.encode([query])[0].tolist()

        # Vraie recherche vectorielle
        results = collection.search(
            data=[query_vector],
            anns_field="embedding",   
            param={"metric_type": "L2", "params": {"nprobe": 10}},
            limit=3
        )

        output = []
        for hits in results:
            for hit in hits:
                entity = hit.entity
                output.append({
                    "id": getattr(entity, "id", None),
                    "opening": getattr(entity, "opening", "Unknown"),
                    "score": float(hit.score)
                })

       
        if output:
            return output

    except Exception as e:
        print("Milvus error → fallback:", e)

    # Sinon fallback
    return _fallback(query)