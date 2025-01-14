# Sudoku Game README

This README provides details on how to set up and play the Sudoku game created using Python's Tkinter module.

---

## Game Overview

This application is a 9x9 Sudoku game where players must fill in the grid following standard Sudoku rules. The game has a countdown timer, limited mistakes allowed, and interactive gameplay.

### Key Features:
- Dynamic grid generation with unique puzzles.
- Timer-based challenge (default: 5 minutes).
- Mistakes are tracked (limit: 3 mistakes).
- Responsive UI for interaction using mouse and keyboard.
- Game over and restart options.

---

## Prerequisites

- Python 3.7 or higher
- Tkinter module (pre-installed with Python)

---

## Installation

1. Clone or download the project files to your local machine.
2. Ensure Python is installed and accessible via the terminal/command prompt.
3. Navigate to the folder containing the script.
4. Run the game with the following command:
   ```
   python sudoku_game.py
   ```

---

## Gameplay Instructions

1. **Starting the Game:**
   - Run the script to start the game. The Sudoku grid will generate randomly.

2. **Filling the Grid:**
   - Click on a cell to select it.
   - Type a number between 1-9 to fill the cell.
   - Use Backspace or Delete to clear the selected cell.

3. **Rules:**
   - Each number must appear exactly once in each row, column, and 3x3 subgrid.
   - You have 3 chances to input incorrect numbers.

4. **Timer:**
   - You have 5 minutes to solve the puzzle. The timer is displayed at the bottom of the window.

5. **Game Over:**
   - The game ends if the timer reaches 0 or you exceed 3 mistakes.
   - A restart button is available to play again.

---

## Code Structure

- **Grid Generation:**
  - Uses algorithms to generate unique Sudoku puzzles and ensure solvability.

- **Timer:**
  - Countdown timer updates every second.

- **UI Design:**
  - Built using the Tkinter canvas for interactive elements.

- **Event Handling:**
  - Handles mouse clicks and keyboard inputs to play the game.
