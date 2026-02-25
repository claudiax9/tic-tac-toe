# Tic Tac Toe – Python Project

## Description

This project is a **Python implementation of Tic Tac Toe**. It includes both a console version and a graphical interface using **Tkinter**, along with an AI that supports multiple difficulty levels.

Features:

* Place X and O symbols on a 3×3 grid.
* Detect the winner or a tie.
* Interactive GUI with clickable buttons.
* AI with random and optimal (minimax) modes.
* Keeps cumulative score across rounds.

---

## Features by Phase

### **Phase 1 – Board & Rules**

* 3×3 grid with X and O players.
* Tracks the current player’s turn.
* Valid move enforcement (cell must be empty).
* Detects a winner or tie.
* Console display of the grid.

### **Phase 2 – GUI (Tkinter)**

* Window with a clickable 3×3 grid.
* Highlights the current player.
* Click to place a symbol; clicks on occupied cells are ignored.
* Status bar shows turn information and game results.
* “Play Again” button resets the board.

### **Phase 3 – AI & Difficulty**

* **Random AI:** selects moves randomly among available cells.
* **Best AI:** chooses optimal moves using the minimax algorithm.
* Difficulty selector: random, alternating, best.
* Best AI never loses; alternating mode changes AI strength visibly.

### **Phase 4 – Game Flow & Scoring**

* Tracks cumulative score: X wins, O wins, ties.
* Displays the winner after each game and allows replay.
* Scores update correctly across multiple games.

---

## How to Run

1. Clone the repository:

   ```bash
   git clone https://github.com/claudiax9/python-class-project.git
   ```
2. Navigate to the project directory:

   ```bash
   cd python-class-project
   ```
3. Run the game:

   ```bash
   python main.py
   ```
4. Follow the instructions in the GUI or console.

---

## Requirements

* Python 3.x
* Tkinter (usually included with Python)
