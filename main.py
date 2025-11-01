from src.toss import toss
from src.match import play_innings
from src.metrics_logger import MetricsLogger
from rich.console import Console
from rich.panel import Panel

console = Console()

def play_match():
    console.print(Panel("[bold green]Welcome to Hand Cricket vs LLM![/]", expand=False))
    user_bats_first = toss()
    metrics = MetricsLogger()

    if user_bats_first:
        user_score, _ = play_innings(True, metrics_logger=metrics)
        console.print(Panel(f" Target for LLM: [bold yellow]{user_score + 1}[/] runs!"))
        llm_score, _ = play_innings(False, target=user_score + 1, metrics_logger=metrics)
    else:
        llm_score, _ = play_innings(False, metrics_logger=metrics)
        console.print(Panel(f" Target for You: [bold yellow]{llm_score + 1}[/] runs!"))
        user_score, _ = play_innings(True, target=llm_score + 1, metrics_logger=metrics)

    console.rule("[bold white] MATCH RESULT[/]")

    if user_score > llm_score:
        console.print("[bold green] You win![/]")
    elif llm_score > user_score:
        console.print("[bold red] LLM wins![/]")
    else:
        console.print("[bold yellow] Match tied![/]")

if __name__ == "__main__":
    play_match()