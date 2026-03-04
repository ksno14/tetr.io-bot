# TETR.IO Bot

An AI agent that autonomously plays Tetris on [TETR.IO](https://tetr.io/) using computer vision and intelligent decision-making.

---

## Group Information

| Field        | Detail                                               |
|--------------|------------------------------------------------------|
| **Group**    | Grupo Scripters                                      |
| **Members**  | Juan Sebastián Umaña Camacho, Samuel Emanuel Daniel Alvarez Torres |
| **Language** | Python 3.14                                          |

---

## Project Structure

```
tetris-ai/
├── vision.py       
├── controller.py   
├── grid.py         
├── config.py       
├── ai.py           
└── main.py         
```

### Module Descriptions

**`vision.py`** — Handles all screen capture and image processing. Responsible for detecting the current Tetris grid, identifying active and upcoming pieces, and translating pixel data into a structured game state the agent can reason about.

**`controller.py`** — Manages keyboard input simulation. Translates high-level move decisions from the AI into actual key presses sent to the TETR.IO browser tab.

**`grid.py`** — Maintains the agent's internal model of the Tetris board. Tracks occupied cells, simulates piece placements, and provides utility methods for evaluating board positions.

**`config.py`** — Centralized configuration file. Contains constants such as grid dimensions, timing parameters, key bindings, capture regions, and AI tuning values.

**`ai.py`** — Core intelligence of the agent. Evaluates possible piece placements using heuristics (e.g., aggregate height, number of holes, bumpiness) and selects the optimal move.

**`main.py`** — The main entry point. Instantiates the agent, coordinates the vision, AI, and controller modules, and runs the main game loop.

---

## Requirements

- **[uv](https://docs.astral.sh/uv/)** — Fast Python package and project manager (required)
- Python 3.14
- A Chromium-based or Firefox browser with [TETR.IO](https://tetr.io/) open

 **Installing uv:** Follow the official instructions at [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/ksno14/tetr.io-bot.git
cd tetr.io_bot
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Run the agent

```bash
uv run main.py
```

> Make sure TETR.IO is open in your browser and the game window is visible before launching the agent.

---

