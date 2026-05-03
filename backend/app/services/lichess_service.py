import requests


def get_theoretical_moves(fen: str):
    try:
        url = f"https://explorer.lichess.ovh/lichess?fen={fen}"
        response = requests.get(url)

        data = response.json()

        moves = []
        for move in data.get("moves", []):
            moves.append(move["san"])

        return moves[:5]

    except Exception as e:
        print("Erreur Lichess :", e)
        return []