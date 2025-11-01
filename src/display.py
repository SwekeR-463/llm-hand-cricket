from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def display_turn(your_move, llm_move):
    table = Table(title="This Turn", show_lines=True)
    table.add_column("You", justify="center", style="bold cyan")
    table.add_column("LLM", justify="center", style="bold magenta")
    table.add_row(str(your_move), str(llm_move))
    console.print(table)

def show_summary(env, label="Innings Summary"):
    table = Table(title=f" {label}", show_lines=True)
    table.add_column("Turn", justify="center")
    table.add_column("Your Move", justify="center")
    table.add_column("LLM Move", justify="center")

    for i, (u, l) in enumerate(env.history):
        table.add_row(str(i + 1), str(u), str(l))

    console.print(table)
    console.print(Panel(f"[bold green]Final Score:[/] {env.score}", expand=False))