import pygame
import os

BASE_DIR = os.path.dirname(__file__)
IMG_DIR = os.path.join(BASE_DIR, "sprites")

def img(nome):
    return os.path.join(IMG_DIR, 'espinho.png')


class RectVermelho:
    def __init__(self, x, y, w, h, image_name=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.image = None

        if image_name:
            try:
                self.image = pygame.image.load(img(image_name)).convert_alpha()
                self.image = pygame.transform.scale(self.image, (w, h))
            except Exception:
                self.image = None

    def draw(self, surface, offset_x):
        draw_rect = pygame.Rect(self.rect)
        draw_rect.x -= offset_x

        if self.image:
            surface.blit(self.image, draw_rect.topleft)
        else:
            pygame.draw.rect(surface, (255, 0, 0), draw_rect)
