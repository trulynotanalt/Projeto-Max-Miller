import pygame



pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600



LEFT_WALL_X = 0
LEFT_WALL_OPEN_Y = 150



MIN_WORLD_X = -350
#
MIN_OFFSET_X = -350

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo do Platman")


INTRO_MUSIC = "sons_musicas/musicainicial.mp3"
pygame.mixer.music.set_volume(0.4) 
GAME_MUSIC = "sons_musicas/jogomusica.mp3"



WHITE = (255, 255, 255)
BLUE = (0, 120, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 215, 0)
BROWN = (139, 69, 19)
PURPLE = (128, 0, 128)
ORANGE = (255, 140, 0)
RED = (255, 0, 0)



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


try:
    som_pulo = pygame.mixer.Sound("sons_musicas/pulo.mp3")
    som_pulo.set_volume(0.3)
except Exception:
    som_pulo = type("FakeSound", (), {"play": lambda *a, **k: None})()

try:
    som_reset = pygame.mixer.Sound("sons_musicas/reset.mp3")
    som_reset.set_volume(0.3)
except Exception:
    som_reset = type("FakeSound", (), {"play": lambda *a, **k: None})()

try:
    kill = pygame.mixer.Sound("sons_musicas/reset.mp3")
    kill.set_volume(0.3)
except Exception:
    kill = type("FakeSound", (), {"play": lambda *a, **k: None})()



SHOOT_SFX_PATH = "sons_musicas/somarma.wav"       
PICKUP_GUN_SFX_PATH = "sons_musicas/pegaarma.mp3"  

try:
    som_tiro = pygame.mixer.Sound(SHOOT_SFX_PATH)
    som_tiro.set_volume(0.35)
except Exception:
    som_tiro = type("FakeSound", (), {"play": lambda *a, **k: None})()

try:
    som_pegar_arma = pygame.mixer.Sound(PICKUP_GUN_SFX_PATH)
    som_pegar_arma.set_volume(0.35)
except Exception:
    som_pegar_arma = type("FakeSound", (), {"play": lambda *a, **k: None})()



SPRITE_PATHS = [
    "sprites/sprite_0.png",
    "sprites/sprite_1.png",
    
]



PORTAL_START_SPRITE = "sprites/pnormal.png"
PORTAL_EXIT_SPRITE  = "sprites/pnormal.png" 


PORTAL_START_SPRITE_SIZE = (120, 160)
PORTAL_EXIT_SPRITE_SIZE  = (120, 160)


PORTAL_START_SPRITE_OFFSET = (-40, -40)
PORTAL_EXIT_SPRITE_OFFSET  = (-40, -40)




ENEMY_SPRITE_LEFT  = "sprites/lacaioE.png"
ENEMY_SPRITE_RIGHT = "sprites/lacaioR.png"


ENEMY_SPRITE_SIZE = (120, 150)


ENEMY_SPRITE_OFFSET = (-40, -70)


GUN_SPRITE = "sprites/arma.png"
BULLET_SPRITE = "sprites/bala.png"

GUN_SIZE = (40, 20)
BULLET_SIZE = (12, 6)

BULLET_SPEED = 10


def safe_load_sprite(path, size):
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, size)
    except Exception:
        s = pygame.Surface(size, pygame.SRCALPHA)
        s.fill((255, 0, 255, 150))
        return s
    

