# Cyberpunk Tic-Tac-Toe // Neon Grid v.77 👾

A highly customized, retro-futuristic Tic-Tac-Toe engine built entirely in Python using the `tkinter` Canvas. This project moves beyond standard GUI widgets, featuring a custom-built rendering engine, particle physics, and an unbeatable AI.

## 🚀 Features

- **Advanced Minimax AI:** Features three difficulty tiers. The "Psycho" (Hard) mode utilizes the Minimax algorithm, making the AI mathematically impossible to beat.
- **Custom Physics Engine:** Includes a lightweight particle system for ambient dust, cell explosions, and dynamic UI interactions.
- **Asynchronous Audio (`SoundSynth`):** Multi-threaded synthesized retro sound effects that run without interrupting the main game loop.
- **Cyberpunk Visuals:** Custom-drawn neon graphics, CRT scanline overlays, and randomized visual glitch filters.
- **Netrunner Hacking Scanner:** A specialized HUD toggle that calculates and displays the real-time win/loss/tie probability of any empty cell using Minimax lookahead.
- **Simulation Mode (EVE):** Watch the AI battle itself in an automated, continuous loop.

## 🛠️ Prerequisites

This project uses Python's standard libraries, meaning no external dependencies (like Pygame) are required!

- Python 3.x
- Windows OS (Required for the `winsound` audio module. The game will still run on macOS/Linux, but audio will be silently disabled).

## 🎮 How to Run

1. Clone the repository:
   ```bash
   git clone [https://github.com/Kirtesh86/cyber-tac-toe.git](https://github.com/Kirtesh86/cyber-tac-toe.git)
   ```
