import pygame
import os
from config import DARK_GREEN, GREEN

BASE_DIR = os.path.dirname(__file__) if "__file__" in globals() else os.getcwd()
SPRITES_DIR = os.path.join(BASE_DIR, "sprites")

def img(nome: str) -> str:
    return os.path.join(SPRITES_DIR, nome)

try:
    PLATFORM_IMG = pygame.image.load(img("plataforma.png")).convert_alpha()
except Exception:
    PLATFORM_IMG = None

PLATFORM_CACHE = {}

def get_platform_texture(width, height, extra_w=0, extra_h=0, filename=None):
    img_w = width + extra_w
    img_h = height + extra_h

    key = (filename, img_w, img_h)
    if key in PLATFORM_CACHE:
        return PLATFORM_CACHE[key]

    surf = None
    if filename:
        try:
            surf = pygame.image.load(img(filename)).convert_alpha()
        except Exception:
            surf = None
    else:
        surf = PLATFORM_IMG

    if surf is not None:
        try:
            tex = pygame.transform.scale(surf, (img_w, img_h))
        except Exception:
            tex = pygame.Surface((img_w, img_h))
            tex.fill(DARK_GREEN)
    else:
        tex = pygame.Surface((img_w, img_h))
        tex.fill(GREEN)

    PLATFORM_CACHE[key] = tex
    return tex
