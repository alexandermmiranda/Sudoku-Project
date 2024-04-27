import pygame

class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.selected = False
        self.font = pygame.font.Font(None, 36)
        self.cell_width = 50
        self.cell_height = 50
        self.x = col * self.cell_width
        self.y = row * self.cell_height

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        # Draw cell
        cell_rect = pygame.Rect(self.x, self.y, self.cell_width, self.cell_height)
        pygame.draw.rect(self.screen, (255, 255, 255), cell_rect)
        
        # Draw value inside cell
        if self.value != 0:
            text_surface = self.font.render(str(self.value), True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(self.x + self.cell_width // 2, self.y + self.cell_height // 2))
            self.screen.blit(text_surface, text_rect)
        
        # Draw red outline if selected
        if self.selected:
            pygame.draw.rect(self.screen, (255, 0, 0), cell_rect, 3)
