# plataformas.py
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, DARK_GREEN, GREEN

# tenta carregar imagem única para plataformas; se não existir, usar retângulos coloridos
try:
    PLATFORM_IMG = pygame.image.load("plataformas.png").convert_alpha()
except Exception:
    PLATFORM_IMG = None

PLATFORM_CACHE = {}

def get_platform_texture(width, height):
    """
    Retorna uma superfície escalada com cache para evitar recálculos.
    """
    key = (width, height)
    tex = PLATFORM_CACHE.get(key)
    if tex is not None:
        return tex
    if PLATFORM_IMG is not None:
        try:
            tex = pygame.transform.scale(PLATFORM_IMG, (width, height))
        except Exception:
            tex = pygame.Surface((width, height))
            tex.fill(DARK_GREEN)
    else:
        tex = pygame.Surface((width, height))
        tex.fill(GREEN)
    PLATFORM_CACHE[key] = tex
    return tex
