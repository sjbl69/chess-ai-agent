import subprocess


def evaluate_position(fen: str):
    try:
        process = subprocess.Popen(
            ["stockfish"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        process.stdin.write(f"position fen {fen}\n")
        process.stdin.write("go depth 10\n")
        process.stdin.write("quit\n")

        output = process.communicate()[0]

        best_move = None
        score = 0

        for line in output.split("\n"):
            if "bestmove" in line:
                best_move = line.split(" ")[1]

        return {
            "score": score,
            "best_move": best_move
        }

    except Exception as e:
        print("Stockfish crash :", e)
        return {
            "score": 0,
            "best_move": "e4"
        }