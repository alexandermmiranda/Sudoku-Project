import pygame
import sys
import sudoku_generator
from sudoku_generator import generate_sudoku
import board

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