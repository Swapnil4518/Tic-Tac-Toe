# Tic-Tac-Toe AI — Mini Project

A web-based Tic-Tac-Toe game built with Python, Flask, HTML, CSS, and JavaScript. It includes Player vs AI, Two Players, and a 10-game AI-vs-random tournament.

## Requirements
- Python 3.9+
- Internet connection is optional for gameplay; Google Fonts are only used for typography.

## Run on Windows
1. Extract the ZIP and open this folder in VS Code.
2. Open the terminal in this folder.
3. Install the dependency:
   ```powershell
   py -m pip install -r requirements.txt
   ```
4. Start the application:
   ```powershell
   py app.py
   ```
5. Open `http://127.0.0.1:5000` in your browser.

If `py` does not work, use `python` instead.

## Features
- Minimax AI searches the game tree to depth 9 and plays optimally.
- Player vs AI and local two-player mode.
- Scoreboard for wins and draws.
- Simulates 10 games against a random opponent and reports AI wins, draws, and losses.
- Responsive UI for laptop and mobile.

## Project structure
```
tic_tac_toe_ai/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js
```

## Algorithm
Minimax recursively tests available moves. It gives the AI a positive score for a win, a negative score for a loss, and zero for a draw. The AI chooses the move with the highest score.
