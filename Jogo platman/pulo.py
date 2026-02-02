import pygame
from config import safe_load_sprite

class RectAzul:
    def __init__(self, x, y, w, h, sprite_path='sprites/doublejump.png'):
        self.rect = pygame.Rect(x, y, w, h)
        self.active = True

        self.image = None
        if sprite_path:
            self.image = safe_load_sprite(sprite_path, (w, h))

    def draw(self, surface, offset_x):
        if not self.active:
            return

        draw_x = self.rect.x - offset_x
        draw_y = self.rect.y

        if self.image:
            surface.blit(self.image, (draw_x, draw_y))
        else:
            pygame.draw.rect(
                surface,
                (0, 120, 255),
                (draw_x, draw_y, self.rect.w, self.rect.h)
            )
