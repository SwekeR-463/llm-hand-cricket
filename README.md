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

This with the `nvidia/nemotron-nano-9b-v2:free`.

```bash
╭─────────────────────────────────╮
│ Welcome to Hand Cricket vs LLM! │
╰─────────────────────────────────╯
╭───────────────────────────────────────────────────────────────────╮
│  Time for the Toss!                                               │
╰───────────────────────────────────────────────────────────────────╯
Call heads or tails: tails
The coin landed on heads!
 LLM won the toss!
LLM chooses to bat first.
────────────────────── Let’s Begin the Match! ───────────────────────
 You are bowling!
Your move (1–6): 6
  This Turn  
┏━━━━━┳━━━━━┓
┃ You ┃ LLM ┃
┡━━━━━╇━━━━━┩
│  6  │  3  │
└─────┴─────┘
╭──────────────────╮
│ Current Score: 3 │
╰──────────────────╯
Your move (1–6): 2
  This Turn  
┏━━━━━┳━━━━━┓
┃ You ┃ LLM ┃
┡━━━━━╇━━━━━┩
│  2  │  5  │
└─────┴─────┘
╭──────────────────╮
│ Current Score: 8 │
╰──────────────────╯
Your move (1–6): 1
  This Turn  
┏━━━━━┳━━━━━┓
┃ You ┃ LLM ┃
┡━━━━━╇━━━━━┩
│  1  │  4  │
└─────┴─────┘
╭───────────────────╮
│ Current Score: 12 │
╰───────────────────╯
Your move (1–6): 1
  This Turn  
┏━━━━━┳━━━━━┓
┃ You ┃ LLM ┃
┡━━━━━╇━━━━━┩
│  1  │  1  │
└─────┴─────┘
╭───────────────────╮
│ Current Score: 12 │
╰───────────────────╯

 OUT!
        Innings Summary        
┏━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Turn ┃ Your Move ┃ LLM Move ┃
┡━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━┩
│  1   │     6     │    3     │
├──────┼───────────┼──────────┤
│  2   │     2     │    5     │
├──────┼───────────┼──────────┤
│  3   │     1     │    4     │
├──────┼───────────┼──────────┤
│  4   │     1     │    1     │
└──────┴───────────┴──────────┘
╭─────────────────╮
│ Final Score: 12 │
╰─────────────────╯
╭───────────────────────────────────────────────────────────────────╮
│  Target for You: 13 runs!                                         │
╰───────────────────────────────────────────────────────────────────╯
 You are batting!
Your move (1–6): 4
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
Failed to reach the target!
───────────────────────────  MATCH RESULT ───────────────────────────
 LLM wins!
```

---

### Todos

- [ ] Add scorecard history and stats tracking
- [ ] Add parsers for getting reasoning traces and the move what LLM chose
- [ ] Add leaderboard for different model's scores against me
- [ ] Enable LLM vs LLM matches
- [ ] Add support for models using HF
- [ ] Web-based UI

---