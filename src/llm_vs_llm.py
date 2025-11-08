import time
from rich.console import Console
from rich.panel import Panel
from .env import HandCricketEnv
from .llm_agent import LLMPlayer
from .display import display_turn, show_summary
from .metrics_logger import MetricsLogger

console = Console()

def play_llm_innings(batter: LLMPlayer, bowler: LLMPlayer, target=None, metrics_logger=None):
    env = HandCricketEnv(user_batting=True)
    env.reset()

    console.print(Panel(f"[bold green]{batter.name} is batting against {bowler.name}![/]"))

    while True:
        start = time.time()
        bat_move = batter.decide_move(env.history)
        bowl_move = bowler.decide_move(env.history)
        latency = time.time() - start

        display_turn(bat_move, bowl_move)
        reward, done, info = env.step(bat_move, bowl_move)
        env.render()

        if metrics_logger:
            metrics_logger.log_turn(
                role=batter.name,
                turn=len(env.history),
                user_move=bat_move,
                llm_move=bowl_move,
                score=info["score"],
                done=done,
                latency=latency,
            )

        if target is not None and info["score"] >= target:
            console.print(Panel(f"[bold green]{batter.name} reached the target![/]"))
            return info["score"], True

        if done:
            console.print(f"[bold red]{batter.name} is OUT![/]")
            show_summary(env, f"{batter.name}'s Innings")
            return info["score"], info["score"] >= (target or 0)


def llm_vs_llm_match(model_a: str, model_b: str):
    console.print(Panel("[bold cyan] LLM vs LLM Hand Cricket Begins![/]"))
    metrics = MetricsLogger()

    llm1 = LLMPlayer("Model-A", model_a, role="batting")
    llm2 = LLMPlayer("Model-B", model_b, role="bowling")

    # Innings 1
    score1, _ = play_llm_innings(llm1, llm2, metrics_logger=metrics)
    console.print(Panel(f"Target for {llm2.name}: [bold yellow]{score1 + 1}[/] runs!"))

    # Swap roles
    llm1.role, llm2.role = "bowling", "batting"
    score2, _ = play_llm_innings(llm2, llm1, target=score1 + 1, metrics_logger=metrics)

    console.rule("[bold white] MATCH RESULT[/]")

    if score2 > score1:
        console.print(f"[bold green]{llm2.name} wins by chasing the target![/]")
    elif score1 > score2:
        console.print(f"[bold red]{llm1.name} wins by defending the total![/]")
    else:
        console.print("[bold yellow]Match tied![/]")
