from rich.console import Console
from rich.panel import Panel
from src.match import play_innings
from src.toss import toss
from src.metrics_logger import MetricsLogger
from src.llm_vs_llm import play_llm_innings as llm_vs_llm_match
from src.series import series

from datetime import datetime

def generate_match_id(prefix="M"):
    return f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


console = Console()

def play_match():
    console.print(Panel("[bold green]Welcome to Hand Cricket Arena![/]", expand=False))
    mode = input("Choose mode (1=You vs LLM, 2=LLM vs LLM, 3=Benchmark 3 matches): ").strip()

    if mode == "3":
        model_a = input("Enter Model-A (e.g., deepseek/deepseek-r1-0528-qwen3-8b:free): ").strip()
        model_b = input("Enter Model-B (e.g., z-ai/glm-4.5-air:free): ").strip()
        match_id = generate_match_id(prefix="BENCH")
        series(model_a, model_b, n_matches=3)
        return

    if mode == "2":
        model_a = input("Enter Model-A (e.g., deepseek/deepseek-r1-0528-qwen3-8b:free): ").strip()
        model_b = input("Enter Model-B (e.g., z-ai/glm-4.5-air:free): ").strip()
        llm_vs_llm_match(model_a, model_b)
        return

    # fallback to user vs llm
    metrics = MetricsLogger()
    user_bats_first = toss()

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
    