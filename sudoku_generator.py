import pygame
import sys
import board
import random
import math

"""
This was adapted from a GeeksforGeeks article "Program for Sudoku Generator" by Aarti_Rathi and Ankur Trisal
https://www.geeksforgeeks.org/program-sudoku-generator/

"""

class SudokuGenerator:
    '''
	create a sudoku board - initialize class variables and set up the 2D board
	This should initialize:
	self.row_length		- the length of each row
	self.removed_cells	- the total number of cells to be removed
	self.board			- a 2D list of ints to represent the board
	self.box_length		- the square root of row_length

	Parameters:
    row_length is the number of rows/columns of the board (always 9 for this project)
    removed_cells is an integer value - the number of cells to be removed

	Return:
	None
    '''
    def __init__(self, row_length=9, removed_cells=40):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = [[0] * row_length for _ in range(row_length)]
        self.box_length = int(math.sqrt(row_length))

    '''
	Returns a 2D python list of numbers which represents the board

	Parameters: None
	Return: list[list]
    '''
    def get_board(self):
        return self.board

    '''
	Displays the board to the console
    This is not strictly required, but it may be useful for debugging purposes

	Parameters: None
	Return: None
    '''
    def print_board(self):
        for row in self.board:
            print(' '.join(str(cell) if cell != 0 else '.' for cell in row))
        print()

    '''
	Determines if num is contained in the specified row (horizontal) of the board
    If num is already in the specified row, return False. Otherwise, return True

	Parameters:
	row is the index of the row we are checking
	num is the value we are looking for in the row
	
	Return: boolean
    '''
    def valid_in_row(self, row, num):
        return num not in self.board[row]

    '''
	Determines if num is contained in the specified column (vertical) of the board
    If num is already in the specified col, return False. Otherwise, return True

	Parameters:
	col is the index of the column we are checking
	num is the value we are looking for in the column
	
	Return: boolean
    '''
    def valid_in_col(self, col, num):
        for row in range(self.row_length):
            if self.board[row][col] == num:
                return False
        return True

    '''
	Determines if num is contained in the 3x3 box specified on the board
    If num is in the specified box starting at (row_start, col_start), return False.
    Otherwise, return True

	Parameters:
	row_start and col_start are the starting indices of the box to check
	i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)
	num is the value we are looking for in the box

	Return: boolean
    '''
    def valid_in_box(self, row_start, col_start, num):
        for i in range(3):
            for j in range(3):
                if self.board[row_start + i][col_start + j] == num:
                    return False
        return True
    
    '''
    Determines if it is valid to enter num at (row, col) in the board
    This is done by checking that num is unused in the appropriate, row, column, and box

	Parameters:
	row and col are the row index and col index of the cell to check in the board
	num is the value to test if it is safe to enter in this cell

	Return: boolean
    '''
    def is_valid(self, row, col, num):
        box_start_row = row - row % 3
        box_start_col = col - col % 3
        return (self.valid_in_row(row, num) and
                self.valid_in_col(col, num) and
                self.valid_in_box(box_start_row, box_start_col, num))

    '''
    Fills the specified 3x3 box with values
    For each position, generates a random digit which has not yet been used in the box

	Parameters:
	row_start and col_start are the starting indices of the box to check
	i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)

	Return: None
    '''
    def fill_box(self, row_start, col_start):
        numbers = list(range(1, self.row_length + 1))
        random.shuffle(numbers)
        for i in range(3):
            for j in range(3):
                self.board[row_start + i][col_start + j] = numbers.pop()
    
    '''
    Fills the three boxes along the main diagonal of the board
    These are the boxes which start at (0,0), (3,3), and (6,6)

	Parameters: None
	Return: None
    '''
    def fill_diagonal(self):
        for i in range(0, self.row_length, 3):
            self.fill_box(i, i)
    '''
    DO NOT CHANGE
    Provided for students
    Fills the remaining cells of the board
    Should be called after the diagonal boxes have been filled
	
	Parameters:
	row, col specify the coordinates of the first empty (0) cell

	Return:
	boolean (whether or not we could solve the board)
    '''
    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True
        
        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    '''
    DO NOT CHANGE
    Provided for students
    Constructs a solution by calling fill_diagonal and fill_remaining

	Parameters: None
	Return: None
    '''
    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    '''
    Removes the appropriate number of cells from the board
    This is done by setting some values to 0
    Should be called after the entire solution has been constructed
    i.e. after fill_values has been called
    
    NOTE: Be careful not to 'remove' the same cell multiple times
    i.e. if a cell is already 0, it cannot be removed again

	Parameters: None
	Return: None
    '''
    def remove_cells(self):
        count = 0
        while count < self.removed_cells:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                count += 1

'''
DO NOT CHANGE
Provided for students
Given a number of rows and number of cells to remove, this function:
1. creates a SudokuGenerator
2. fills its values and saves this as the solved state
3. removes the appropriate number of cells
4. returns the representative 2D Python Lists of the board and solution

Parameters:
size is the number of rows/columns of the board (9 for this project)
removed is the number of cells to clear (set to 0)

Return: list[list] (a 2D Python list to represent the board)
'''
def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 700
GRID_SIZE = SCREEN_WIDTH // 9
FONT = pygame.font.Font(None, 40)
BIG_FONT = pygame.font.Font(None, 60)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
HIGHLIGHT = (100, 200, 255)
BLUE = (0, 0, 255)


# Setup display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sudoku")


# Helper functions
def draw_text(text, font, color, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_obj, text_rect)


def draw_button(text, x, y, width, height, color, text_color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    draw_text(text, FONT, text_color, x + width // 2, y + height // 2)


def main_menu():
    button_rects = {
        "easy": pygame.Rect(150, 250, 300, 50),
        "medium": pygame.Rect(150, 325, 300, 50),
        "hard": pygame.Rect(150, 400, 300, 50)
    }
    running = True
    while running:
        screen.fill(WHITE)
        draw_text("Sudoku Game", BIG_FONT, BLACK, SCREEN_WIDTH // 2, 100)
        for key, rect in button_rects.items():
            draw_button(key.capitalize(), rect.x, rect.y, rect.width, rect.height, LIGHT_GRAY, BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for difficulty, rect in button_rects.items():
                    if rect.collidepoint(event.pos):
                        num_empty = 30 if difficulty == "easy" else 40 if difficulty == "medium" else 50
                        game_loop(num_empty)

        pygame.display.update()


def game_loop(empty_cells):
    current_board = generate_sudoku(9, empty_cells)  # Assume this returns a single board
    initial_board = [row[:] for row in current_board]  # Create a deep copy for resetting

    selected_cell = None
    game_over = False
    win = False

    def reset_board():
        nonlocal current_board
        current_board = [row[:] for row in initial_board]  # Reset to original puzzle state

    def check_solution():
        nonlocal game_over, win
#need to implement check_board from richards board
        win = is_solution_correct(current_board)
        game_over = True

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_click(event.pos)
            elif event.type == pygame.KEYDOWN and selected_cell and not game_over:
                handle_key_press(event, selected_cell)

        screen.fill(WHITE)
        draw_grid()
        draw_numbers(current_board, selected_cell)
        draw_buttons()
        pygame.display.update()

    draw_end_screen(win)

def handle_mouse_click(position):
    global selected_cell
    x, y = position
    if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_WIDTH:  # Click within the grid
        selected_cell = (y // GRID_SIZE, x // GRID_SIZE)
    elif reset_button_rect.collidepoint(position):
        reset_board()
    elif restart_button_rect.collidepoint(position):
        main_menu()
    elif exit_button_rect.collidepoint(position):
        pygame.quit()
        sys.exit()

def handle_key_press(event, selected_cell):
    if event.unicode.isdigit():
        num = int(event.unicode)
        if 1 <= num <= 9:
            row, col = selected_cell
            if current_board[row][col] == 0:  # Make sure the cell can be edited
                current_board[row][col] = num
                if is_full(current_board):
                    check_solution()

def draw_grid():
    for i in range(10):
        width = 3 if i % 3 == 0 else 1
        pygame.draw.line(screen, BLACK, (i * GRID_SIZE, 0), (i * GRID_SIZE, SCREEN_WIDTH), width)
        pygame.draw.line(screen, BLACK, (0, i * GRID_SIZE), (SCREEN_WIDTH, i * GRID_SIZE), width)


def draw_numbers(board, selected_cell):
    for row in range(9):
        for col in range(9):
            cell_value = board[row][col]
            if cell_value != 0:
                color = BLACK if (row, col) != selected_cell else HIGHLIGHT
                draw_text(str(cell_value), FONT, color, col * GRID_SIZE + GRID_SIZE // 2,
                          row * GRID_SIZE + GRID_SIZE // 2)

def draw_buttons():
    global reset_button_rect, restart_button_rect, exit_button_rect
    reset_button_rect = pygame.Rect(50, 620, 100, 40)
    restart_button_rect = pygame.Rect(200, 620, 100, 40)
    exit_button_rect = pygame.Rect(350, 620, 100, 40)
    draw_button("Reset", reset_button_rect.x, reset_button_rect.y, reset_button_rect.width, reset_button_rect.height, BLUE, WHITE)
    draw_button("Restart", restart_button_rect.x, restart_button_rect.y, restart_button_rect.width, restart_button_rect.height, BLUE, WHITE)
    draw_button("Exit", exit_button_rect.x, exit_button_rect.y, exit_button_rect.width, exit_button_rect.height, BLUE, WHITE)

def draw_end_screen(win):
    screen.fill(WHITE)
    message = "Congratulations, You Win!" if win else "Game Over: Try Again!"
    draw_text(message, BIG_FONT, RED if not win else GREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pygame.display.update()
    pygame.time.wait(3000)  # Display end screen for 3 seconds
    main_menu()

def is_full(board):
    return all(all(cell != 0 for cell in row) for row in board)


if __name__ == "__main__":
    main_menu()

