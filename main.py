import os
import random
import time
import requests
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from dotenv import load_dotenv

load_dotenv()

# config

USE_LLM = True
MODEL_NAME = "z-ai/glm-4.5-air:free"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

console = Console()

# game env

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

# llm moves

def llm_reasoning(history, role="bowling"):
    if not USE_LLM or not OPENROUTER_API_KEY:
        return random.randint(1, 6)

    history_text = "\n".join(
        [f"Turn {i+1}: You={u}, LLM={l}" for i, (u, l) in enumerate(history)]
    ) or "No previous turns yet."

    if role == "bowling":
        prompt = f"""
You are playing hand cricket as the bowler.
Your goal is to get the opponent OUT by predicting their number (1 - 6).
Think step by step about what the opponent might choose based on history.
Then finally give your number as "Move: X".

Game history:
{history_text}
"""
    else:
        prompt = f"""
You are batting in hand cricket.
Your goal is to score runs by choosing a number (1 - 6) that’s different from what the opponent might pick.
Think step by step about the bowler’s likely move, then give your final number as "Move: X".

Game history:
{history_text}
"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "http://localhost/",
            "X-Title": "HandCricketEnv",
        },
        json={
            "model": MODEL_NAME,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.9,
        },
        timeout=20,
    )

    data = response.json()
    text = data["choices"][0]["message"]["content"].strip()

    # split reasoning and final move
    if "Move:" in text:
        reasoning, move_part = text.split("Move:", 1)
        console.print(Panel(f"[italic blue]LLM Thinking...[/]\n{reasoning.strip()}", expand=False))
        text = move_part.strip()
    else:
        console.print(Panel(f"[italic blue]LLM Thinking... (brief output)[/]\n{text}", expand=False))

    move = int("".join([ch for ch in text if ch.isdigit()]) or random.randint(1, 6))
    if move < 1 or move > 6:
        move = random.randint(1, 6)

    console.print(f"[bold magenta]LLM decides to play:[/] {move}")
    return move

# display helper

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


# toss

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


# innings helper

def play_innings(user_batting, target=None):
    env = HandCricketEnv(user_batting)
    env.reset()

    if user_batting:
        console.print("[bold yellow] You are batting![/]")
        role = "bowling"
    else:
        console.print("[bold blue] You are bowling![/]")
        role = "batting"

    while True:
        your_move = int(input("Your move (1–6): "))
        if your_move < 1 or your_move > 6:
            console.print("[red]Enter a valid number between 1–6![/]")
            continue

        llm_move = llm_reasoning(env.history, role=role)
        time.sleep(0.3)
        display_turn(your_move, llm_move)

        reward, done, info = env.step(your_move, llm_move)
        env.render()

        if target is not None:
            if info["score"] >= target:
                console.print(Panel("[bold green] Target Reached![/]"))
                return info["score"], True

        if done:
            console.print("\n [bold red]OUT![/]")
            show_summary(env)
            if target is not None:
                if info["score"] >= target:
                    console.print("[bold green]You reached the target before getting out![/]")
                    return info["score"], True
                else:
                    console.print("[bold red]Failed to reach the target![/]")
                    return info["score"], False
            return info["score"], False


# full match flow

def play_match():
    console.print(Panel("[bold green]Welcome to Hand Cricket vs LLM![/]", expand=False))
    user_bats_first = toss()

    if user_bats_first:
        user_score, _ = play_innings(user_batting=True)
        console.print(Panel(f" Target for LLM: [bold yellow]{user_score + 1}[/] runs!"))
        llm_score, chased = play_innings(user_batting=False, target=user_score + 1)
    else:
        llm_score, _ = play_innings(user_batting=False)
        console.print(Panel(f" Target for You: [bold yellow]{llm_score + 1}[/] runs!"))
        user_score, chased = play_innings(user_batting=True, target=llm_score + 1)

    console.rule("[bold white] MATCH RESULT[/]")

    if user_bats_first:
        if llm_score >= user_score + 1:
            console.print("[bold red] LLM wins by chasing the target![/]")
        elif llm_score < user_score:
            console.print("[bold green] You win![/]")
        else:
            console.print("[bold yellow] Match tied![/]")
    else:
        if user_score >= llm_score + 1:
            console.print("[bold green] You win by chasing the target![/]")
        elif user_score < llm_score:
            console.print("[bold red] LLM wins![/]")
        else:
            console.print("[bold yellow] Match tied![/]")


if __name__ == "__main__":
    play_match()
