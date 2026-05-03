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

        commands = f"""
position fen {fen}
go depth 10
"""

        process.stdin.write(commands)
        process.stdin.flush()

        best_move = "e4"
        score = 0

        while True:
            line = process.stdout.readline()

            if "score cp" in line:
                parts = line.split()
                if "cp" in parts:
                    score = int(parts[parts.index("cp") + 1]) / 100

            if "bestmove" in line:
                best_move = line.split()[1]
                break

        process.terminate()

        return {
            "score": score,
            "best_move": best_move
        }

    except Exception:
        
        return {
            "score": 0,
            "best_move": "e4"
        }