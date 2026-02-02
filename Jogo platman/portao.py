# portao.py
import pygame
from config import PURPLE, WHITE, safe_load_sprite


class Gate:
  
    def __init__(
        self,
        x,
        y,
        width=40,
        height=80,
        color=PURPLE,
        sprite_path=None,
        sprite_size=None,
        sprite_offset=(0, 0),
    ):
      
        self.rect = pygame.Rect(x, y, width, height)

        self.color = color
        self.sprite_offset = sprite_offset

      
        self.image = None
        if sprite_path:
            draw_size = sprite_size if sprite_size is not None else (width, height)
            self.image = safe_load_sprite(sprite_path, draw_size)

    def draw(self, surface, offset_x):
        draw_x = self.rect.x - offset_x
        draw_y = self.rect.y

        if self.image:
            off_x, off_y = self.sprite_offset
            surface.blit(self.image, (draw_x + off_x, draw_y + off_y))
        else:
           
            draw_rect = pygame.Rect(self.rect)
            draw_rect.x -= offset_x
            pygame.draw.rect(surface, self.color, draw_rect)
            inner_rect = pygame.Rect(draw_rect.x + 5, draw_rect.y + 10,
                                     self.rect.width - 10, self.rect.height - 20)
            pygame.draw.rect(surface, WHITE, inner_rect)
