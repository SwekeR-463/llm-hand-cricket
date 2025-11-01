## Hand Cricket vs LLM

*A fully interactive CLI hand cricket match between me and a LLM!*

Play a complete two-innings hand cricket match complete with toss, target chasing, and realistic win/loss logic against an AI opponent powered by OpenRouter models.

---

### Features

* **Toss system** - choose to bat or bowl first
* **Two innings** - one for you, one for the LLM
* **Real cricket logic** - whoever successfully chases the target wins
* **CLI visuals** using [`rich`](https://github.com/Textualize/rich)
* **LLM opponent** using OpenRouter Models
* **Fallback random mode** when no API key is set
* **Win detection** when target is reached

---


### Setup & Run (with `uv`)

**Install [`uv`](https://docs.astral.sh/uv/getting-started/):**

```bash
pip install uv
```

**Clone the repository:**

```bash
git clone https://github.com/SwekeR-463/llm-hand-cricket.git
cd llm-hand-cricket
```

**Create and sync environment using `uv`:**

```bash
uv init
uv sync
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

**Set your OpenRouter API key:**

Directly setup

```bash
export OPENROUTER_API_KEY="your_openrouter_api_key_here"
```

Else setup `.env`
```bash
touch .env
```
And add
```env
OPENROUTER_API_KEY="your_api_key_here"
```

If not set, the random move mode will be used.

**Run the match:**

```bash
uv run main.py
```

---

### How to Play

1. The game begins with a **toss**, where you call “heads” or “tails”.
2. If you win the toss, choose to bat or bowl first.
3. Enter a number between **1 - 6** on every ball:
    * If both pick the **same number**, it’s **OUT!**
    * Otherwise, runs are added (your move when batting, LLM’s when bowling).
4. The second innings begins with a **target**.
5. The first side to **chase or defend successfully** wins!

---

### Example Run

This is with the `nvidia/nemotron-nano-9b-v2:free`.

```bash
╭─────────────────────────────────╮
│ Welcome to Hand Cricket vs LLM! │
╰─────────────────────────────────╯
╭───────────────────────────────────────────────────────────────────╮
│  Time for the Toss!                                               │
╰───────────────────────────────────────────────────────────────────╯
Call heads or tails: heds
The coin landed on tails!
 LLM won the toss!
LLM chooses to bowl first.
────────────────────── Let’s Begin the Match! ───────────────────────
You are batting!
Your move (1–6): 4
╭───────────────────────────────────────────────────────────────────╮
│ > LLM Thinking...                                                 │
│ Since this is the first turn with no historical data, I need to   │
│ choose a number without prior information. As the bowler, my goal │
│ is to strategically increase the probability of getting the       │
│ batsman out (scoring pick the same number) to end the innings and │
│ prevent any runs from being scored. At the same time, I should    │
│ minimize the potential runs scored if the numbers differ.         │
│                                                                   │
│ Assuming the user might choose a number randomly or based on      │
│ common tendencies (like avoiding extremes or choosing "lucky"     │
│ numbers), I'll select a moderate number—specifically, 4. This is  │
│ because numbers around the middle of the range (3-5) are often    │
│ perceived as balanced and less risky. Choosing 4 gives me a 1/6   │
│ chance of getting an out, and if not out, the user scores 4,      │
│ which is moderate and not a high-scoring number. This approach    │
│ helps me avoid extreme outcomes while keeping the game            │
│ interesting.                                                      │
╰───────────────────────────────────────────────────────────────────╯
- LLM plays: 4
  This Turn  
┏━━━━━┳━━━━━┓
┃ You ┃ LLM ┃
┡━━━━━╇━━━━━┩
│  4  │  4  │
└─────┴─────┘
╭──────────────────╮
│ Current Score: 0 │
╰──────────────────╯

 OUT!
        Innings Summary        
┏━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Turn ┃ Your Move ┃ LLM Move ┃
┡━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━┩
│  1   │     4     │    4     │
└──────┴───────────┴──────────┘
╭────────────────╮
│ Final Score: 0 │
╰────────────────╯
╭───────────────────────────────────────────────────────────────────╮
│  Target for LLM: 1 runs!                                          │
╰───────────────────────────────────────────────────────────────────╯
You are bowling!
Your move (1–6): 3
╭───────────────────────────────────────────────────────────────────╮
│ > LLM Thinking...                                                 │
│ As the AI batting in this one-on-one hand cricket match, I need   │
│ to start strategically with no prior history to predict the       │
│ user's choices. Since there's no data, I'll assume the user is    │
│ choosing randomly or with common human tendencies, which often    │
│ favor numbers between 3 and 5 for a balance of scoring potential  │
│ and risk avoidance (e.g., avoiding 1 for low scores and 6 for     │
│ higher dismissal risk).                                           │
│                                                                   │
│ For my first move, I aim for a number that maximizes expected     │
│ runs while not being too extreme. Calculating the expected value  │
│ with a random user choice (each number has a 1/6 probability),    │
│ the expected runs for number X are (5/6) * X. For X=5, this gives │
│ approximately 4.17 runs, which is high but not the extreme of X=6 │
│ (5 expected runs). However, X=6 has a higher risk of dismissal,   │
│ so I'll opt for 5 as a compromise between high scoring and        │
│ moderate risk.                                                    │
│                                                                   │
│ This choice also allows me to potentially score runs quickly      │
│ while setting up future strategic plays based on the user's       │
│ response. I'll keep an eye on their next move to adjust my        │
│ strategy—e.g., if they often choose high numbers, I might vary my │
│ choices to avoid patterns.                                        │
╰───────────────────────────────────────────────────────────────────╯
- LLM plays: 5
  This Turn  
┏━━━━━┳━━━━━┓
┃ You ┃ LLM ┃
┡━━━━━╇━━━━━┩
│  3  │  5  │
└─────┴─────┘
╭──────────────────╮
│ Current Score: 5 │
╰──────────────────╯
╭───────────────────────────────────────────────────────────────────╮
│  Target Reached!                                                  │
╰───────────────────────────────────────────────────────────────────╯
───────────────────────────  MATCH RESULT ───────────────────────────
 LLM wins!
```

---

### Todos

- [x] Make everything under `src/`
- [ ] Add scorecard history and stats tracking
- [ ] Add parsers for getting reasoning traces and the move what LLM chose
- [ ] Add leaderboard for different model's scores against me
- [ ] Enable LLM vs LLM matches
- [ ] Add support for models using HF
- [ ] Add support for Cerebras endpoints
- [ ] Web-based UI

---