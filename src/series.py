from datetime import datetime
import statistics
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from .llm_agent import LLMPlayer
from .metrics_logger import MetricsLogger
from .llm_vs_llm import play_llm_innings
from .env import HandCricketEnv

console = Console()

def run_single_match(model_a: str, model_b: str, match_id: str):
    metrics = MetricsLogger(match_id=match_id)
    llm1 = LLMPlayer("Model-A", model_a, role="batting")
    llm2 = LLMPlayer("Model-B", model_b, role="bowling")

    env = HandCricketEnv(user_batting=True)
    score1, _ = play_llm_innings(llm1, llm2, metrics_logger=metrics, match_id=match_id, innings="1st")
    target = score1 + 1

    llm1.role, llm2.role = "bowling", "batting"
    score2, _ = play_llm_innings(llm2, llm1, target=target, metrics_logger=metrics, match_id=match_id, innings="2nd")

    winner = "Model-A" if score1 > score2 else "Model-B" if score2 > score1 else "Tie"
    margin = abs(score1 - score2)
    return {"model_a_score": score1, "model_b_score": score2, "winner": winner, "margin": margin}


def series(model_a: str, model_b: str, n_matches: int = 3):
    """
    Runs multiple matches and aggregates benchmark statistics.
    """
    console.print(Panel(f"[bold cyan] Benchmark of 3 matches: {model_a} vs {model_b}[/]", expand=False))
    results = []

    for i in range(1, n_matches + 1):
        match_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i:03d}"
        console.rule(f"[bold yellow]Match {i}[/]")
        result = run_single_match(model_a, model_b, match_id)
        results.append(result)


    # Aggregate stats
    model_a_wins = sum(1 for r in results if r["winner"] == "Model-A")
    model_b_wins = sum(1 for r in results if r["winner"] == "Model-B")
    ties = sum(1 for r in results if r["winner"] == "Tie")

    avg_a = statistics.mean([r["model_a_score"] for r in results])
    avg_b = statistics.mean([r["model_b_score"] for r in results])
    avg_margin = statistics.mean([r["margin"] for r in results])

    # Display summary
    console.rule("[bold white] Benchmark Summary[/]")

    table = Table(title=f"{model_a} vs {model_b} (n={n_matches})", show_lines=True)
    table.add_column("Metric", justify="left", style="bold cyan")
    table.add_column("Value", justify="center", style="bold yellow")

    table.add_row("Matches Played", str(n_matches))
    table.add_row("Model-A Wins", str(model_a_wins))
    table.add_row("Model-B Wins", str(model_b_wins))
    table.add_row("Ties", str(ties))
    table.add_row("Avg Score (Model-A)", f"{avg_a:.2f}")
    table.add_row("Avg Score (Model-B)", f"{avg_b:.2f}")
    table.add_row("Avg Margin", f"{avg_margin:.2f}")

    console.print(table)

    # Determine series winner
    if model_a_wins > model_b_wins:
        console.print(Panel(f" [bold green]{model_a} wins the series![/]"))
    elif model_b_wins > model_a_wins:
        console.print(Panel(f" [bold red]{model_b} wins the series![/]"))
    else:
        console.print(Panel(" [bold yellow]Series tied![/]"))

    return results
