import pygame
from pulo import Pulo

class PlatWoman(Pulo):
    def __init__(self, x, y, w, h, sprite_path='sprites/platwomanD.png'):
        super().__init__(x, y, w, h, sprite_path)
        self.image = pygame.transform.flip(self.image, True, False)
