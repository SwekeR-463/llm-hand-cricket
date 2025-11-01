import json
import time

class MetricsLogger:
    def __init__(self, filename="match_metrics.jsonl"):
        self.filename = filename

    def log_turn(self, role, turn, user_move, llm_move, score, done, latency):
        entry = {
            "timestamp": time.time(),
            "role": role,
            "turn": turn,
            "user_move": user_move,
            "llm_move": llm_move,
            "score": score,
            "done": done,
            "latency": latency,
        }
        with open(self.filename, "a") as f:
            f.write(json.dumps(entry) + "\n")