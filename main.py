import pygame
from sudoku_generator import generate_sudoku
from board import Board

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 540, 600
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

# Game state
game_board = None
difficulty = None
running = True

def draw_text(text, font, color, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    screen.blit(text_obj, text_rect)

def main_menu():
    global game_board, difficulty
    button_rects = {
        "easy": pygame.Rect(150, 250, 240, 50),
        "medium": pygame.Rect(150, 325, 240, 50),
        "hard": pygame.Rect(150, 400, 240, 50)
    }
    while True:
        screen.fill(WHITE)
        draw_text("Sudoku Game", BIG_FONT, BLACK, SCREEN_WIDTH // 2, 100)
        for key, rect in button_rects.items():
            pygame.draw.rect(screen, LIGHT_GRAY, rect)
            draw_text(key.capitalize(), FONT, BLACK, rect.centerx, rect.centery)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for diff, rect in button_rects.items():
                    if rect.collidepoint(event.pos):
                        difficulty = diff
                        game_board = Board(SCREEN_WIDTH, SCREEN_HEIGHT, screen, difficulty)
                        game_loop()

        pygame.display.update()

def game_loop():
    global running
    while running:
        screen.fill(WHITE)
        game_board.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                game_board.select(*game_board.click(*pos))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_board.place_number(game_board.cells[game_board.selected_cell[0]][game_board.selected_cell[1]].sketch)
                elif event.key == pygame.K_BACKSPACE:
                    game_board.clear()
                elif event.unicode.isdigit():
                    num = int(event.unicode)
                    if 1 <= num <= 9:
                        game_board.sketch(num)

        pygame.display.update()

if __name__ == "__main__":
    main_menu()
