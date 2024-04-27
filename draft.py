import pygame
import sys
import sudoku_generator
from sudoku_generator import generate_sudoku
import board
import random
import math

# Define the Cell class
class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.cell_width = 60
        self.cell_height = 60
        self.x = col * self.cell_width + 50
        self.y = row * self.cell_height + 50

    def draw(self):
        # Draw cell
        pygame.draw.rect(self.screen, (255, 255, 255), (self.x, self.y, self.cell_width, self.cell_height))
        
        # Draw value inside cell
        if self.value != 0:
            text_surface = self.font.render(str(self.value), True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(self.x + self.cell_width // 2, self.y + self.cell_height // 2))
            self.screen.blit(text_surface, text_rect)
        
        # Draw border
        pygame.draw.rect(self.screen, (0, 0, 0), (self.x, self.y, self.cell_width, self.cell_height), 1)

# Initialize Pygame and set up the display
pygame.init()
screen = pygame.display.set_mode((600, 700))
pygame.display.set_caption('Sudoku')
font = pygame.font.Font(None, 36)

# Colors and button definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (180, 180, 180)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

difficulty_settings = {'easy': 30, 'medium': 40, 'hard': 50}
current_board = None
selected_cell = None
running = True
game_state = 'start'

# Button areas for difficulty selection and control
button_easy = pygame.Rect(150, 250, 300, 50)
button_medium = pygame.Rect(150, 325, 300, 50)
button_hard = pygame.Rect(150, 400, 300, 50)
reset_button = pygame.Rect(50, 650, 100, 50)
restart_button = pygame.Rect(250, 650, 100, 50)
exit_button = pygame.Rect(450, 650, 100, 50)

def draw_button(screen, text, rect, color, text_color):
    pygame.draw.rect(screen, color, rect)
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def draw_board(screen, board):
    for row in range(9):
        for col in range(9):
            value = board[row][col]
            x = col * 60 + 50
            y = row * 60 + 50
            pygame.draw.rect(screen, WHITE, (x, y, 60, 60))
            if value != 0:
                text_surf = font.render(str(value), True, BLACK)
                text_rect = text_surf.get_rect(center=(x + 30, y + 30))
                screen.blit(text_surf, text_rect)
            pygame.draw.rect(screen, BLACK, (x, y, 60, 60), 1)

def generate_sudoku(difficulty):
    # Placeholder for generating a sudoku board based on difficulty
    # This function should interact with your Sudoku generator logic
    return [[0]*9 for _ in range(9)]

def check_solution(board):
    # Placeholder for solution checking logic
    return True

def main():
    global current_board, running, game_state, selected_cell
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if game_state == 'start':
                    if button_easy.collidepoint(x, y):
                        current_board = generate_sudoku(9, difficulty_settings['easy'])
                        game_state = 'game'
                    elif button_medium.collidepoint(x, y):
                        current_board = generate_sudoku(9, difficulty_settings['medium'])
                        game_state = 'game'
                    elif button_hard.collidepoint(x, y):
                        current_board = generate_sudoku(9, difficulty_settings['hard'])
                        game_state = 'game'
                elif game_state == 'game':
                    if reset_button.collidepoint(x, y):
                        current_board = generate_sudoku(current_difficulty)
                    elif restart_button.collidepoint(x, y):
                        game_state = 'start'
                    elif exit_button.collidepoint(x, y):
                        running = False
                    elif 50 <= x <= 590 and 50 <= y <= 590:  # Board area
                        col = (x - 50) // 60
                        row = (y - 50) // 60
                        selected_cell = (row, col)
            elif event.type == pygame.KEYDOWN and selected_cell:
                if event.unicode.isdigit():
                    row, col = selected_cell
                    current_board[row][col] = int(event.unicode)
                    if check_solution(current_board):
                        game_state = 'end'

        screen.fill(LIGHT_GRAY)
        if game_state == 'start':
            draw_button(screen, 'Easy', button_easy, GRAY, BLACK)
            draw_button(screen, 'Medium', button_medium, GRAY, BLACK)
            draw_button(screen, 'Hard', button_hard, GRAY, BLACK)
        elif game_state in ['game', 'end']:
            draw_board(screen, current_board)
            draw_button(screen, 'Reset', reset_button, GRAY, BLACK)
            draw_button(screen, 'Restart', restart_button, GRAY, BLACK)
            draw_button(screen, 'Exit', exit_button, GRAY, BLACK)
            if game_state == 'end':
                text_surf = font.render('Sudoku Solved!', True, GREEN)
                text_rect = text_surf.get_rect(center=(300, 650))
                screen.blit(text_surf, text_rect)

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
