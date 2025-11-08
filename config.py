import pygame

# Tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo do Platman com tela inicial")

# Cores
WHITE = (255, 255, 255)
BLUE = (0, 120, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 215, 0)
BROWN = (139, 69, 19)
SKIN = (255, 224, 189)
PURPLE = (128, 0, 128)
ORANGE = (255, 140, 0)

# FPS e Clock
FPS = 60
CLOCK = pygame.time.Clock()

# Player
PLATMAN_WIDTH = 40
PLATMAN_HEIGHT = 60
MOVE_SPEED = 5
JUMP_SPEED = 9
GRAVITY = 0.8
MAX_JUMP_TIME = 15
MAX_JUMP_HEIGHT = 150

# Fade
FADE_IN_DURATION = 1000
