import pygame
import random

pygame.font.init()


class Button:
    def __init__(self, text, x, y, width, height, color, font_size):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.font_size = font_size

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", self.font_size)
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text,
                 (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def is_hover(self, pos):
        return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height


class Cell:
    def __init__(self, x, y, value=0):
        self.x = x
        self.y = y
        self.value = value
        self.width = 50
        self.height = 50

    def draw(self, win, selected):
        if selected:
            pygame.draw.rect(win, (255, 0, 0), (self.x - 1, self.y - 1, self.width + 2, self.height + 2), 3)  # Red outline when selected
        else:
            pygame.draw.rect(win, (255, 255, 255), (self.x - 1, self.y - 1, self.width + 2, self.height + 2), 2)  # Grid outline

        if self.value != 0:
            font = pygame.font.SysFont("comicsans", 30)
            text = font.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                            self.y + (self.height / 2 - text.get_height() / 2)))

        # Draw grid outline inside the cell
        pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, self.width, self.height), 1)


class GameStartScreen:
    def __init__(self, win):
        self.win = win
        self.win_width = 450  # New window width
        self.win_height = 700  # New window height
        self.win.fill((255, 255, 255))

        self.title_font = pygame.font.SysFont("comicsans", 60)
        self.title_text = self.title_font.render("Sudoku", True, (0, 0, 0))
        self.title_rect = self.title_text.get_rect(center=(self.win_width // 2, 100))  # Center the title

        self.button_font = pygame.font.SysFont("comicsans", 30)
        self.buttons = [
            Button("Easy", self.win_width // 2 - 50, 300, 100, 50, (0, 255, 0), 30),
            Button("Medium", self.win_width // 2 - 50, 400, 100, 50, (255, 165, 0), 30),
            Button("Hard", self.win_width // 2 - 50, 500, 100, 50, (255, 0, 0), 30)
        ]
        self.difficulty = None

    def draw(self):
        self.win.blit(self.title_text, self.title_rect)  # Draw the title

        for button in self.buttons:
            button.draw(self.win)  # Draw the buttons

    def handle_click(self, pos):
        for button in self.buttons:
            if button.is_hover(pos):
                self.difficulty = button.text.lower()
                return self.difficulty
        return None



class Board:
    def __init__(self, rows, cols, win):
        self.rows = rows
        self.cols = cols
        self.initial_board = None  # Store the initial state of the board
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.selected = None
        self.win = win
        self.cell_width = 50
        self.cell_height = 50

    def draw(self):
        # Draw outer grid lines and bold lines every 3 columns and rows
        for i in range(self.rows):
            line_thickness = 4 if i % 3 == 0 and i != 0 else 1
            pygame.draw.line(self.win, (0, 0, 0), (0, i * self.cell_height),
                             (self.cols * self.cell_width, i * self.cell_height), line_thickness)
        pygame.draw.line(self.win, (0, 0, 0), (0, self.rows * self.cell_height),
                         (self.cols * self.cell_width, self.rows * self.cell_height), 4)  # Bottom bold line

        for j in range(self.cols):
            line_thickness = 4 if j % 3 == 0 and j != 0 else 1
            pygame.draw.line(self.win, (0, 0, 0), (j * self.cell_width, 0),
                             (j * self.cell_width, self.rows * self.cell_height), line_thickness)

        # Draw cells
        for i in range(self.rows):
            for j in range(self.cols):
                selected = False
                if self.selected == (i, j):
                    selected = True
                cell = Cell(j * self.cell_width, i * self.cell_height, self.board[i][j])
                cell.draw(self.win, selected)

    def click(self, pos):
        x, y = pos
        row = y // self.cell_height
        col = x // self.cell_width
        self.selected = (row, col)

    def sketch(self, value):
        if self.selected:
            row, col = self.selected
            self.board[row][col] = value

    def reset(self):
        self.board = [row[:] for row in self.initial_board]  # Reset the board to its initial state

    def is_full(self):
        for row in self.board:
            if 0 in row:
                return False
        return True

    def clear(self):
        if self.selected:
            row, col = self.selected
            if self.board[row][col] != 0:
                self.board[row][col] = 0


class SudokuGenerator:
    def __init__(self, win, difficulty):
        self.win = win
        self.difficulty = difficulty
        self.board = Board(9, 9, win)

    def generate_board(self):
        # Generate Sudoku board based on the selected difficulty
        if self.difficulty == "easy":
            empty_cells = 30
        elif self.difficulty == "medium":
            empty_cells = 40
        elif self.difficulty == "hard":
            empty_cells = 50

        self.board.initial_board = self.generate_sudoku_board()  # Store the initial state
        self.board.board = [row[:] for row in self.board.initial_board]  # Set the board to its initial state
        self.remove_cells(empty_cells)

    def generate_sudoku_board(self):
        board = [[0 for _ in range(9)] for _ in range(9)]
        self.fill_values(board)
        return board

    def fill_values(self, board):
        # Helper function to recursively fill the Sudoku board
        def is_valid(board, row, col, num):
            # Check if the number is not already used in current row, column, and subgrid
            for i in range(9):
                if board[row][i] == num or board[i][col] == num or board[(row // 3) * 3 + i // 3][
                    (col // 3) * 3 + i % 3] == num:
                    return False
            return True

        def solve(board):
            for i in range(9):
                for j in range(9):
                    if board[i][j] == 0:
                        for num in range(1, 10):
                            if is_valid(board, i, j, num):
                                board[i][j] = num
                                if solve(board):
                                    return True
                                board[i][j] = 0  # Backtrack
                        return False
            return True

        # Solve the Sudoku board
        solve(board)

    def remove_cells(self, empty_cells):
        # Randomly remove cells to create the puzzle
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        for _ in range(empty_cells):
            row, col = cells.pop()
            self.board.initial_board[row][col] = 0  # Update the initial board as well
            self.board.board[row][col] = 0

    def draw_game_in_progress(self):
        self.win.fill((255, 255, 255))
        self.board.draw()

    def handle_click(self, pos):
        self.board.click(pos)

    def sketch_number(self, value):
        self.board.sketch(value)

    def clear_cell(self):
        self.board.clear()

    def reset_board(self):
        self.board.reset()

    def check_win(self):
        # Check rows
        for row in self.board.board:
            if sorted(row) != list(range(1, 10)):
                return False

        # Check columns
        for col in range(9):
            column_values = [self.board.board[row][col] for row in range(9)]
            if sorted(column_values) != list(range(1, 10)):
                return False

        # Check 3x3 subgrids
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                subgrid_values = []
                for x in range(3):
                    for y in range(3):
                        subgrid_values.append(self.board.board[i + x][j + y])
                if sorted(subgrid_values) != list(range(1, 10)):
                    return False

        return True

    def check_loss(self):
        if self.board.is_full() and not self.check_win():
            return True
        return False


def display_end_screen(win, text):
    win.fill((255, 255, 255))
    font = pygame.font.SysFont("comicsans", 60)
    text_surf = font.render(text, True, (0, 0, 0))
    win.blit(text_surf, (150, 250))
    pygame.display.update()


def main():
    pygame.init()
    win = pygame.display.set_mode((450, 600))
    pygame.display.set_caption("Sudoku")

    game_start_screen = GameStartScreen(win)
    run = True

    difficulty = None  # Ensure the variable is assigned even if the loop is exited without selecting difficulty

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                difficulty = game_start_screen.handle_click(pos)
                if difficulty:
                    run = False  # Exit the loop to start the game

        game_start_screen.draw()
        pygame.display.update()

    sudoku_game = SudokuGenerator(win, difficulty)
    sudoku_game.generate_board()

    # Define buttons
    reset_button = Button("Reset", 50, 520, 100, 50, (0, 255, 0), 30)
    restart_button = Button("Restart", 175, 520, 100, 50, (255, 165, 0), 30)
    exit_button = Button("Exit", 300, 520, 100, 50, (255, 0, 0), 30)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if reset_button.is_hover(pos):
                    sudoku_game.reset_board()  # Reset the board to its initial state
                elif restart_button.is_hover(pos):
                    main()  # Restart the game
                elif exit_button.is_hover(pos):
                    pygame.quit()
                    quit()
                else:
                    sudoku_game.handle_click(pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    sudoku_game.sketch_number(1)
                elif event.key == pygame.K_2:
                    sudoku_game.sketch_number(2)
                elif event.key == pygame.K_3:
                    sudoku_game.sketch_number(3)
                elif event.key == pygame.K_4:
                    sudoku_game.sketch_number(4)
                elif event.key == pygame.K_5:
                    sudoku_game.sketch_number(5)
                elif event.key == pygame.K_6:
                    sudoku_game.sketch_number(6)
                elif event.key == pygame.K_7:
                    sudoku_game.sketch_number(7)
                elif event.key == pygame.K_8:
                    sudoku_game.sketch_number(8)
                elif event.key == pygame.K_9:
                    sudoku_game.sketch_number(9)
                elif event.key == pygame.K_DELETE:
                    sudoku_game.clear_cell()

        sudoku_game.draw_game_in_progress()

        # Check for win condition
        if sudoku_game.check_win():
            display_end_screen(win, "You Win!")
            pygame.time.delay(3000)  # Display the win screen for 3 seconds
            main()  # Restart the game

        # Check for loss condition
        if sudoku_game.check_loss():
            display_end_screen(win, "You Lose!")
            pygame.time.delay(3000)  # Display the loss screen for 3 seconds
            main()  # Restart the game

        # Draw buttons
        reset_button.draw(win)
        restart_button.draw(win)
        exit_button.draw(win)

        pygame.display.update()


if __name__ == "__main__":
    main()

