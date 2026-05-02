"""
Service de recherche vectorielle (version simplifiée sans ML lourd)

Objectif :
- Fournir un endpoint fonctionnel /vector-search
- Éviter les conflits avec transformers / sentence-transformers
- Garantir la stabilité du projet
"""


def search_similar_positions(query: str):
    """
    Simule une recherche vectorielle.

    Args:
        query (str): requête utilisateur (ex: "sicilian defense")

    Returns:
        list: résultats simulés
    """

    # 🔒 sécurité basique
    if not query or len(query.strip()) == 0:
        return []

    query = query.lower()

    # 🧠 logique simulée (tu peux adapter)
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

    elif "caro" in query:
        return [
            {"id": 5, "opening": "Caro-Kann Defense", "score": 0.94},
            {"id": 6, "opening": "Classical Variation", "score": 0.89},
        ]

    # 🎯 fallback générique
    return [
        {"id": 0, "opening": "Unknown Opening", "score": 0.80}
    ]