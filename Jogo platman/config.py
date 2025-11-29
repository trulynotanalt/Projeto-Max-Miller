# config.py
import pygame


# Inicialização
pygame.init()

# --- janela ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo do Platman")

# --- músicas ---
INTRO_MUSIC = "musicaintro1.mp3"
GAME_MUSIC = "musicamaingame.mp3"

# --- cores ---
WHITE = (255, 255, 255)
BLUE = (0, 120, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 215, 0)
BROWN = (139, 69, 19)
PURPLE = (128, 0, 128)
ORANGE = (255, 140, 0)

# --- constantes ---
FPS = 60
CLOCK = pygame.time.Clock()
PLATMAN_WIDTH = 40
PLATMAN_HEIGHT = 60
MOVE_SPEED = 5
JUMP_SPEED = 9
GRAVITY = 0.8
MAX_JUMP_TIME = 15
MAX_JUMP_HEIGHT = 150
FADE_IN_DURATION = 1000
PLAYER_ANIM_INTERVAL_MS = 5000

_current_music = None

# --- música funções ---
def play_music(path, loops=-1):
    global _current_music
    try:
        if path is None:
            pygame.mixer.music.stop()
            _current_music = None
            return
        if _current_music == path:
            return
        pygame.mixer.music.stop()
        try:
            pygame.mixer.music.unload()
        except Exception:
            pass
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(loops)
        _current_music = path
    except Exception:
        _current_music = None

# --- sons (robustos caso os arquivos não existam) ---
try:
    som_pulo = pygame.mixer.Sound("pulo.mp3")
except Exception:
    som_pulo = type("FakeSound", (), {"play": lambda *a, **k: None})()

try:
    som_reset = pygame.mixer.Sound("reset.mp3")
except Exception:
    som_reset = type("FakeSound", (), {"play": lambda *a, **k: None})()

try:
    kill = pygame.mixer.Sound("morte_inimigo.mp3")
except Exception:
    kill = type("FakeSound", (), {"play": lambda *a, **k: None})()

# --- sprites ---
SPRITE_PATHS = [
    "sprites/sprite0_0.png",
    "sprites/sprite0_1.png",
]

def safe_load_sprite(path, size):
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, size)
    except Exception:
        s = pygame.Surface(size, pygame.SRCALPHA)
        s.fill((255, 0, 255, 150))
        return s
