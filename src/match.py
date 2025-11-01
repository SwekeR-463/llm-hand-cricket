import time
from .env import HandCricketEnv
from .llm_agent import llm_reasoning
from .display import display_turn, show_summary
from .metrics_logger import MetricsLogger
from rich.console import Console
from rich.panel import Panel

console = Console()

def play_innings(user_batting, target=None, metrics_logger=None):
    env = HandCricketEnv(user_batting)
    env.reset()
    role = "bowling" if user_batting else "batting"

    console.print(f"[bold yellow]{'You are batting!' if user_batting else 'You are bowling!'}[/]")

    while True:
        your_move = int(input("Your move (1–6): "))
        start = time.time()
        llm_move = llm_reasoning(env.history, role=role)
        latency = time.time() - start

        display_turn(your_move, llm_move)
        reward, done, info = env.step(your_move, llm_move)
        env.render()

        if metrics_logger:
            metrics_logger.log_turn(role, len(env.history), your_move, llm_move, info["score"], done, latency)

        if target is not None and info["score"] >= target:
            console.print(Panel("[bold green] Target Reached![/]"))
            return info["score"], True

        if done:
            console.print("\n [bold red]OUT![/]")
            show_summary(env)
            if target is not None:
                return info["score"], info["score"] >= target
            return info["score"], False