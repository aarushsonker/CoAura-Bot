## CoAura Simulation Console

A small interactive reactor-simulation demo built with Gradio. Play the role of the Commander and respond to CoAura — the chatbot that drives the simulation. The UI runs in your browser and uses a simple chat-like interface with choice buttons.

### Features

- Interactive decision tree driven simulation
- Simple chat-based UI (Gradio)
- Restartable scenarios and random outcomes for replayability

### Prerequisites

- Python 3.8 or newer
- pip

The project uses Gradio for the UI. If you plan to develop or run locally, create a virtual environment first.

### Quick start (Windows / PowerShell)

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Upgrade pip and install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install gradio
```

3. Run the app:

```powershell
python main.py
```

After launching, Gradio will print a local URL (for example http://127.0.0.1:7860) — open it in your browser to play.

### How to play

- All bot messages come from CoAura (the chatbot). You won't see separate "system" prompt messages — CoAura speaks directly to the player.
- Read CoAura's messages in the chat area (Mission Feed).
- Choose an action from the radio buttons and click Submit.
- Watch system health and messages; if the reactor fails you can restart the simulation.

### Example conversation

An example mission feed might look like:

```
CoAura: 🧠 System online. Reactor instability detected, Commander.
You: Run diagnostics
CoAura: Coolant system at 43% integrity. What now?
You: Patch coolant system
CoAura: Patch successful. Reactor stabilizing. ✅
```

This README and the UI present CoAura as the single chatbot voice for clarity.

### Notes & next steps

- Consider adding a `requirements.txt` or `pyproject.toml` to pin dependencies.
- Add tests for the game logic (the functions `progress` and `reset_game`).
- Add basic CI to run linting/tests.

### License

This repository includes a `LICENSE` file — see it for license details.

---
