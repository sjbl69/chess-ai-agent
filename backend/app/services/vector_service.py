"""
Vector Search Service

Objectif :
- Fournir une recherche vectorielle pour les ouvertures d’échecs
- Version actuelle simulée (POC)
- Structure prête pour intégration Milvus

Note:
L'intégration Milvus pourra remplacer la logique simulée sans modifier l'API.
"""

from typing import List, Dict


def search_similar_positions(query: str) -> List[Dict]:
    """
    Recherche des positions similaires (simulation vectorielle)

    Args:
        query (str): requête utilisateur (ex: "sicilian defense")

    Returns:
        list: liste de résultats similaires
    """

    # 🔒 sécurité
    if not query or not isinstance(query, str):
        return []

    query = query.lower().strip()

    # 🧠 Simulation de recherche vectorielle
    # (remplaçable par Milvus ou autre DB vectorielle)

    if "sicilian" in query:
        return [
            {
                "id": 1,
                "opening": "Sicilian Defense",
                "score": 0.95
            },
            {
                "id": 2,
                "opening": "Najdorf Variation",
                "score": 0.92
            }
        ]

    elif "french" in query:
        return [
            {
                "id": 3,
                "opening": "French Defense",
                "score": 0.96
            },
            {
                "id": 4,
                "opening": "Advance Variation",
                "score": 0.90
            }
        ]

    elif "caro" in query:
        return [
            {
                "id": 5,
                "opening": "Caro-Kann Defense",
                "score": 0.94
            },
            {
                "id": 6,
                "opening": "Classical Variation",
                "score": 0.89
            }
        ]

    # 🎯 fallback générique
    return [
        {
            "id": 0,
            "opening": "Unknown Opening",
            "score": 0.80
        }
    ]


# 🧠 FUTURE EXTENSION (Milvus)
"""
Exemple d'intégration future :

from pymilvus import Collection

def search_similar_positions(query: str):
    embedding = encoder.encode(query)
    results = collection.search(embedding)
    return results
"""