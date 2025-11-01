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

    # Prompt: make the LLM believe it's playing against user
    prompt = (
        f"You are an AI cricket player competing in a one-on-one hand cricket match against a human user.\n"
        f"You are currently **{role.upper()}**.\n\n"
        "Rules of the game:\n"
        "- Both you (AI) and the user pick a number between 1 and 6.\n"
        "- If both numbers are the same, the batsman is OUT.\n"
        "- If the numbers are different, the batsman scores runs equal to their chosen number.\n\n"
        "Your goal is to think strategically like a human might — try to predict what the user could pick next.\n"
        "Respond with reasoning and your final move in this format: 'Move: X' (where X is between 1–6).\n\n"
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

        # handle when LLM returns an error response
        if "choices" not in data:
            error_info = data.get("error", {}).get("message", "Unknown API error")
            console.print(Panel(f"[red]LLM API error:[/] {error_info}", expand=False))
            return random.randint(1, 6)

        text = data["choices"][0]["message"]["content"].strip()

        # Extract reasoning if available
        if "Move:" in text:
            reasoning, move_part = text.split("Move:", 1)
            console.print(Panel(f"[italic blue]> LLM Thinking...[/]\n{reasoning.strip()}", expand=False))
            text = move_part.strip()
        else:
            console.print(Panel(f"[italic blue]> LLM Thinking... (brief output)[/]\n{text}", expand=False))

        # Extract digits from response
        move = int("".join([ch for ch in text if ch.isdigit()]) or random.randint(1, 6))
        if move < 1 or move > 6:
            move = random.randint(1, 6)

        console.print(f"[bold magenta]- LLM plays:[/] {move}")
        return move

    except Exception as e:
        console.print(Panel(f"[red]- Error in LLM call:[/] {e}", expand=False))
        return random.randint(1, 6)
