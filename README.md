Sudoku Game

This is a simple Sudoku game implemented in Python using the Pygame library. Sudoku is a popular logic-based puzzle game where the objective is to fill a 9x9 grid with digits so that each column, each row, and each of the nine 3x3 subgrids contain all of the digits from 1 to 9.

Installation

Make sure you have Python installed on your system. You can download it from the official Python website.
Install Pygame by running pip install pygame in your terminal or command prompt.

*How to Play*

Run the sudoku.py file.
The game will start with a difficulty selection screen where you can choose between Easy, Medium, and Hard levels.
Click on the desired difficulty level to start the game.
Use the mouse to click on the cells and keyboard numbers to input your guesses.
Use the "Reset" button to reset the board to its initial state, the "Restart" button to start a new game, and the "Exit" button to quit the game.
The game will automatically detect when you win or lose and prompt you accordingly.

Components

Button Class: Represents clickable buttons used for difficulty selection and game controls.
Cell Class: Represents individual cells in the Sudoku grid.
GameStartScreen Class: Manages the game start screen where difficulty is selected.
Board Class: Handles the logic and drawing of the Sudoku board.
SudokuGenerator Class: Generates Sudoku boards based on difficulty and checks for win/loss conditions.
