import os
import random
import requests
from rich.console import Console
from rich.panel import Panel
from dotenv import load_dotenv

load_dotenv()
console = Console()

USE_LLM = True
MODEL_NAME = "deepseek/deepseek-r1-0528-qwen3-8b:free"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def llm_reasoning(history, role="bowling"):
    """
    Get the LLM's next move based on the current role and game history.
    The LLM believes it is playing against a human user.
    """
    if not USE_LLM or not OPENROUTER_API_KEY:
        return random.randint(1, 6)

    # Format game history
    history_text = "\n".join(
        [f"Turn {i+1}: User={u}, LLM={l}" for i, (u, l) in enumerate(history)]
    ) or "No previous turns yet."

    # Prompt
    prompt = (
        f"You are an AI cricket player competing in a one-on-one hand cricket match against a human user.\n"
        f"You are currently **{role.upper()}**.\n\n"
        "Rules of the game:\n"
        "- Both players pick a number between 1 and 6.\n"
        "- If both numbers are the same, the batsman is OUT.\n"
        "- Otherwise, the batsman scores runs equal to their number.\n\n"
        "Think strategically like a human. Respond with reasoning and your final move as 'Move: X'.\n\n"
        f"Game so far:\n{history_text}\n\n"
        "Now think carefully and choose your next move."
    )

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost/",
                "X-Title": "HandCricketEnv",
            },
            json={
                "model": MODEL_NAME,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.8,
            },
            timeout=25,
        )

        data = response.json()

        if "choices" not in data:
            error_info = data.get("error", {}).get("message", "Unknown API error")
            console.print(Panel(f"[red]LLM API error:[/] {error_info}", expand=False))
            return random.randint(1, 6)

        text = data["choices"][0]["message"]["content"].strip()

        # Split reasoning if provided
        if "Move:" in text:
            reasoning, move_part = text.split("Move:", 1)
            console.print(Panel(f"[italic blue]> LLM Thinking...[/]\n{reasoning.strip()}", expand=False))
            text = move_part.strip()
        else:
            console.print(Panel(f"[italic blue]> LLM Thinking... (brief output)[/]\n{text}", expand=False))

        move = int("".join([ch for ch in text if ch.isdigit()]) or random.randint(1, 6))
        if move < 1 or move > 6:
            move = random.randint(1, 6)

        console.print(f"[bold magenta]- LLM plays:[/] {move}")
        return move

    except Exception as e:
        console.print(Panel(f"[red]- Error in LLM call:[/] {e}", expand=False))
        return random.randint(1, 6)


class LLMPlayer:
    """Wrapper class for LLM players (for LLM vs LLM matches)."""

    def __init__(self, name: str, model_name: str, role: str, use_llm=True):
        self.name = name
        self.model_name = model_name
        self.role = role  # "batting" or "bowling"
        self.use_llm = use_llm

    def decide_move(self, history):
        """Decide next move based on role and game history."""
        if not self.use_llm or not OPENROUTER_API_KEY:
            return random.randint(1, 6)

        history_text = "\n".join(
            [f"Turn {i+1}: Bat={u}, Bowl={l}" for i, (u, l) in enumerate(history)]
        ) or "No previous turns yet."

        prompt = (
            f"You are {self.name}, an AI cricket player currently {self.role.upper()} in a hand cricket match.\n"
            "Both players pick numbers between 1 and 6 each turn.\n"
            "- If both are same, batsman is OUT.\n"
            "- Otherwise, runs = batsman's number.\n"
            "Respond with reasoning and your final number as 'Move: X'.\n\n"
            f"Game so far:\n{history_text}\n\n"
            "Think carefully and pick your move."
        )

        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "http://localhost/",
                    "X-Title": "HandCricketEnv",
                },
                json={
                    "model": self.model_name,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.8,
                },
                timeout=25,
            )

            data = response.json()
            text = data["choices"][0]["message"]["content"].strip()

            if "Move:" in text:
                reasoning, move_part = text.split("Move:", 1)
                console.print(Panel(f"[italic blue]{self.name} thinking...[/]\n{reasoning.strip()}", expand=False))
                text = move_part.strip()

            move = int("".join([ch for ch in text if ch.isdigit()]) or random.randint(1, 6))
            move = move if 1 <= move <= 6 else random.randint(1, 6)

            console.print(f"[bold magenta]{self.name} plays:[/] {move}")
            return move

        except Exception as e:
            console.print(Panel(f"[red]{self.name} error:[/] {e}", expand=False))
            return random.randint(1, 6)
