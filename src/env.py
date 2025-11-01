import random
from rich.panel import Panel
from rich.console import Console

console = Console()

class HandCricketEnv:
    def __init__(self, user_batting=True):
        self.score = 0
        self.done = False
        self.history = []
        self.user_batting = user_batting

    def reset(self):
        self.score = 0
        self.done = False
        self.history = []
        return None

    def step(self, user_move, llm_move):
        if self.user_batting:
            if user_move == llm_move:
                self.done = True
                reward = -1
            else:
                self.score += user_move
                reward = user_move
        else:
            if user_move == llm_move:
                self.done = True
                reward = -1
            else:
                self.score += llm_move
                reward = llm_move

        self.history.append((user_move, llm_move))
        return reward, self.done, {"score": self.score}

    def render(self):
        console.print(Panel(f"[bold yellow]Current Score:[/] {self.score}", expand=False))