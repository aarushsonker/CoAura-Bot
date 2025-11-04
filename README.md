## CoAura — NASA's SOS Response Agent

An interactive space station emergency simulation game built with Gradio. Play as a Commander responding to critical system failures with the help of CoAura — NASA's SOS Response Agent chatbot. The UI runs in your browser with a simple chat-like interface and multiple-choice decisions.

### Features

- **Three critical systems to manage**: Oxygen (O2), Cooling, and Power
- **Multi-level decision trees**: Each system failure has multiple choice paths
- **Random outcomes**: 50% chance of success/failure for added replayability
- **Progressive difficulty**: Fix one system, another fails — complete all three to win
- **Visual state tracking**: `img_state` values (1-7) for future visual enhancements
- Simple chat-based UI powered by Gradio

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

1. **Start the mission**: CoAura will prompt you to run a system scan or ignore warnings
2. **Diagnose the problem**: A random system failure will be detected (O2, Cooling, or Power)
3. **Make decisions**: Choose from two initial approaches to fix the problem
4. **Final choice**: Each approach leads to two sub-options with 50% success rate
5. **Continue or fail**: 
   - Success → System stabilizes, another failure detected
   - Failure → Catastrophic system failure, restart required
6. **Win condition**: Successfully repair all three systems (O2, Cooling, Power)

### Gameplay mechanics

- **System Failures**: Three types randomized each playthrough
  - **Oxygen (O2)**: Valve adjustments or backup rerouting
  - **Cooling**: Flow rate changes or backup loop activation
  - **Power**: Voltage regulation or auxiliary power switching

- **Decision structure**: Each failure has 4 possible outcomes (2×2 choices)
- **Random outcomes**: Each final choice has a 50% chance of success
- **Progressive gameplay**: Complete one system to unlock the next challenge
- **Response delay**: Natural 0.5-1 second pause between bot responses

- **Visual system**: The code includes `img_state` values (1-7) ready for adding spacecraft visuals:
  - `1` = Normal/stable
  - `2` = Oxygen issue (gas leaking)
  - `3` = Cooling issue (freezing)
  - `4` = Power issue (battery malfunction)
  - `5` = System recovering (bandage on spacecraft)
  - `6` = Stable state
  - `7` = Critical failure (spacecraft imploding)
- Consider adding a `requirements.txt` with `gradio` pinned to a specific version
- Add tests for game logic (`progress` and `reset_game` functions)
- Implement visual feedback using `img_state` values
- Add sound effects for immersion
- Add basic CI to run linting/tests

### License

This repository includes a `LICENSE` file — see it for license details.

---
