# portao.py
import pygame
from config import PURPLE, WHITE

class Gate:
    def __init__(self, x, y, width=40, height=80, color=PURPLE):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface, offset_x):
        draw_rect = pygame.Rect(self.rect)
        draw_rect.x -= offset_x
        pygame.draw.rect(surface, self.color, draw_rect)
        inner_rect = pygame.Rect(draw_rect.x + 5, draw_rect.y + 10, self.width - 10, self.height - 20)
        pygame.draw.rect(surface, WHITE, inner_rect)
