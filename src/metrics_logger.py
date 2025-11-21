import json
import os
import time
from datetime import datetime

class MetricsLogger:
    def __init__(self, base_dir="logs", match_id=None):
        os.makedirs(base_dir, exist_ok=True)
        if match_id is None:
            match_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filepath = os.path.join(base_dir, f"match_{match_id}.jsonl")

    def log_turn(
        self, *,
        match_id,
        innings,
        turn,
        batter_name,
        bowler_name,
        batter_move,
        bowler_move,
        score,
        done,
        latency,
        reasoning_batter=None,
        reasoning_bowler=None
    ):
        """Log full per-turn trace with reasoning."""
        entry = {
            "timestamp": time.time(),
            "match_id": match_id,
            "innings": innings,
            "turn": turn,
            "batter": batter_name,
            "bowler": bowler_name,
            "batter_move": batter_move,
            "bowler_move": bowler_move,
            "score": score,
            "done": done,
            "latency": latency,
            "reasoning_batter": reasoning_batter,
            "reasoning_bowler": reasoning_bowler,
        }
        with open(self.filepath, "a") as f:
            f.write(json.dumps(entry) + "\n")
