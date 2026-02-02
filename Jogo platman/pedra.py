from pulo import Pulo

class Pedra(Pulo):
    def __init__(self, x, y, w, h, sprite_path='sprites/espinho.png'):
        super().__init__(x, y, w, h, sprite_path)