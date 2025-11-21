import time
from rich.console import Console
from rich.panel import Panel
from .env import HandCricketEnv
from .display import display_turn, show_summary
from .metrics_logger import MetricsLogger

console = Console()

def play_llm_innings(batter, bowler, target=None, metrics_logger=None, match_id="000", innings="1st"):
    env = HandCricketEnv(user_batting=True)
    env.reset()

    console.print(Panel(f"[bold green]{batter.name} is batting against {bowler.name}![/]"))

    while True:
        start = time.time()
        bat_move, bat_reasoning = batter.decide_move(env.history)
        bowl_move, bowl_reasoning = bowler.decide_move(env.history)
        latency = time.time() - start

        display_turn(bat_move, bowl_move)
        reward, done, info = env.step(bat_move, bowl_move)
        env.render()

        if metrics_logger:
            metrics_logger.log_turn(
                match_id=match_id,
                innings=innings,
                turn=len(env.history),
                batter_name=batter.name,
                bowler_name=bowler.name,
                batter_move=bat_move,
                bowler_move=bowl_move,
                score=info["score"],
                done=done,
                latency=latency,
                reasoning_batter=bat_reasoning,
                reasoning_bowler=bowl_reasoning
            )

        if target is not None and info["score"] >= target:
            console.print(Panel(f"[bold green]{batter.name} reached the target![/]"))
            return info["score"], True

        if done:
            console.print(f"[bold red]{batter.name} is OUT![/]")
            show_summary(env, f"{batter.name}'s Innings")
            return info["score"], info["score"] >= (target or 0)
