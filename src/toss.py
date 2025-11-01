import random
from rich.console import Console
from rich.panel import Panel

console = Console()

def toss():
    console.print(Panel("[bold cyan] Time for the Toss![/]"))
    user_call = input("Call heads or tails: ").strip().lower()
    toss_result = random.choice(["heads", "tails"])
    console.print(f"The coin landed on [bold magenta]{toss_result}[/]!")

    if user_call == toss_result:
        console.print("[bold green] You won the toss![/]")
        choice = input("Do you want to bat or bowl first? (bat/bowl): ").strip().lower()
        user_bats_first = choice == "bat"
    else:
        console.print("[bold red] LLM won the toss![/]")
        llm_choice = random.choice(["bat", "bowl"])
        console.print(f"LLM chooses to [bold yellow]{llm_choice}[/] first.")
        user_bats_first = llm_choice == "bowl"

    console.rule("[bold white]Let’s Begin the Match![/]")
    return user_bats_first