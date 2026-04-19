# Tic Tac Toe

A desktop tic tac toe game built with Python and Tkinter. Play against an AI that uses the minimax algorithm, or play locally with two people on the same machine.

## Requirements

- **Python 3.9+** (tested on 3.12)
- **Tkinter** (included with the standard Windows installer for Python; on Linux you may need `python3-tk`)

No extra packages are required.

## How to run

From a terminal in this folder:

```bash
python ai.py
```

On Windows you can also double-click `ai.py` if `.py` files are associated with Python.

## Features

- **vs Computer** — You play as **X**; the computer plays **O** after each of your moves.
- **2 Players** — Pass-and-play on one keyboard: **X** then **O** alternate turns.
- **AI strength** (vs Computer only)
  - **Easy** — Random legal moves.
  - **Medium** — Mix of random and optimal play.
  - **Hard** — Full minimax (optimal play when the AI moves second).
- **Session scoreboard** — Counts wins for X, wins for O, and draws until you reset or close the app.
- **Sound** (optional) — Short beeps on moves and outcomes on **Windows** only; use **Sound: On / Off** in the header. On other systems the game runs without sound.

## Controls

| Control | Action |
|--------|--------|
| Grid cells | Place your mark (when it is your turn and the cell is empty) |
| **New game** | Clear the board and start a new round (scores are kept) |
| **Reset session scores** | Set all session win/draw counts back to zero |
| **vs Computer** / **2 Players** | Switch mode (also clears the current board) |
| **Easy / Medium / Hard** | Set AI difficulty (only applies in vs Computer) |

## Project layout

```
Tic-Tac-Toe game/
├── ai.py      # Application entry point and all UI + game logic
└── README.md  # This file
```

## License

This project is provided as-is for learning and personal use.
