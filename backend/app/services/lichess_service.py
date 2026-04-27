import requests

LICHESS_API = "https://explorer.lichess.ovh/masters"


def get_theoretical_moves(fen: str):
    try:
        response = requests.get(
            LICHESS_API,
            params={"fen": fen},
            timeout=5
        )
        response.raise_for_status()

        data = response.json()
        moves = data.get("moves", [])

        return [
            {
                "uci": move["uci"],
                "san": move["san"],
                "white": move["white"],
                "draws": move["draws"],
                "black": move["black"]
            }
            for move in moves
        ]

    except requests.exceptions.RequestException:
        return None