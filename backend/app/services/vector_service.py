"""
Vector Search Service

- Utilise Milvus si disponible
- Sinon fallback simulé
- Ne casse jamais l'API
"""

from typing import List, Dict

# tentative import Milvus (optionnel)
try:
    from pymilvus import connections, Collection
    MILVUS_AVAILABLE = True
except:
    MILVUS_AVAILABLE = False


def search_similar_positions(query: str) -> List[Dict]:
    """
    Recherche vectorielle avec fallback
    """

    if not query or not isinstance(query, str):
        return []

    query = query.lower().strip()

    # PARTIE MILVUS (si dispo)

    if MILVUS_AVAILABLE:
        try:
            connections.connect(host="milvus", port="19530")

            collection = Collection("chess_positions")

           
            # On simule une recherche Milvus minimale

            results = collection.query(
                expr="id >= 0",
                limit=2
            )

            if results:
                return [
                    {
                        "id": r.get("id", 0),
                        "opening": "From Milvus",
                        "score": 0.99
                    }
                    for r in results
                ]

        except Exception as e:
            print("Milvus indisponible -> fallback :", e)

    # FALLBACK SIMULÉ

    if "sicilian" in query:
        return [
            {"id": 1, "opening": "Sicilian Defense", "score": 0.95},
            {"id": 2, "opening": "Najdorf Variation", "score": 0.92},
        ]

    elif "french" in query:
        return [
            {"id": 3, "opening": "French Defense", "score": 0.96},
            {"id": 4, "opening": "Advance Variation", "score": 0.90},
        ]

    return [
        {"id": 0, "opening": "Unknown Opening", "score": 0.80}
    ]