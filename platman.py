import pygame
import sys


pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo do Platman com múltiplas fases e portões diferenciados")

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


class Player:
    def __init__(self):
        self.x = 100.0
        self.y = SCREEN_HEIGHT - PLATMAN_HEIGHT - 50
        self.rect = pygame.Rect(int(self.x), int(self.y), PLATMAN_WIDTH, PLATMAN_HEIGHT)
        self.vel_y = 0
        self.on_ground = False
        self.alive = True
        self.jump_time = 0

    def move(self, dx, platforms):
        self.x += dx
        if self.x < 0:
            self.x = 0
        self.rect.x = int(self.x)

        for platform in platforms:
            if self.rect.colliderect(platform):
                if dx > 0:
                    self.rect.right = platform.left
                    self.x = self.rect.x
                elif dx < 0:
                    self.rect.left = platform.right
                    self.x = self.rect.x

    def apply_gravity(self, platforms):
        self.vel_y += GRAVITY
        if self.vel_y > 20:
            self.vel_y = 20
        self.y += self.vel_y
        self.rect.y = int(self.y)

        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.vel_y > 0:
                    self.rect.bottom = platform.top
                    self.y = self.rect.y
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = platform.bottom
                    self.y = self.rect.y
                    self.vel_y = 0

    def jump(self):
        if self.on_ground:
            self.jump_time = 0
            self.vel_y = -JUMP_SPEED

    def update_jump(self, keys):
        if keys[pygame.K_SPACE] or keys[pygame.K_w]:
            if self.jump_time < MAX_JUMP_TIME:
                self.jump_time += 1
                self.vel_y = -JUMP_SPEED * (1 + (self.jump_time / MAX_JUMP_TIME))
                if self.rect.y <= SCREEN_HEIGHT - PLATMAN_HEIGHT - MAX_JUMP_HEIGHT:
                    self.vel_y = -JUMP_SPEED
        else:
            self.jump_time = MAX_JUMP_TIME

    def draw(self, surface, offset_x):
        draw_rect = pygame.Rect(self.rect)
        draw_rect.x -= offset_x
        pygame.draw.rect(surface, WHITE, draw_rect)

        shoe_rect = pygame.Rect(draw_rect.x, draw_rect.y + PLATMAN_HEIGHT - 10, PLATMAN_WIDTH, 10)
        pygame.draw.rect(surface, BLACK, shoe_rect)

        face_center = (draw_rect.x + PLATMAN_WIDTH // 2, draw_rect.y + 20)
        pygame.draw.circle(surface, SKIN, face_center, 12)
        eye_radius = 2
        eye_y = face_center[1] - 2
        pygame.draw.circle(surface, BLACK, (face_center[0] - 5, eye_y), eye_radius)
        pygame.draw.circle(surface, BLACK, (face_center[0] + 5, eye_y), eye_radius)


class Enemy:
    def __init__(self, patrol_platform, speed=2):
        self.patrol_platform = patrol_platform
        self.width = 40
        self.height = 40
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.on_ground = False
        self.alive = True

        self.x = float(self.patrol_platform.left + 10)
        self.y = float(self.patrol_platform.top - self.height)
        self.rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)

        self.patrol_start = self.patrol_platform.left + 5
        self.patrol_end = self.patrol_platform.right - self.width - 5

    def reset(self):
        self.x = float(self.patrol_platform.left + 10)
        self.y = float(self.patrol_platform.top - self.height)
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        self.direction = 1
        self.vel_y = 0
        self.on_ground = False
        self.alive = True

    def apply_gravity(self, platforms):
        self.vel_y += GRAVITY
        if self.vel_y > 20:
            self.vel_y = 20
        self.y += self.vel_y
        self.rect.y = int(self.y)

        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.vel_y > 0:
                    self.rect.bottom = platform.top
                    self.y = self.rect.y
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = platform.bottom
                    self.y = self.rect.y
                    self.vel_y = 0

    def update(self, platforms):
        if not self.alive:
            return

        next_x = self.x + self.speed * self.direction
        if next_x < self.patrol_start:
            self.direction = 1
            next_x = self.patrol_start
        elif next_x > self.patrol_end:
            self.direction = -1
            next_x = self.patrol_end

        self.x = next_x
        self.rect.x = int(self.x)

        self.apply_gravity(platforms)
        if self.rect.bottom > self.patrol_platform.top:
            self.rect.bottom = self.patrol_platform.top
            self.y = self.rect.y
            self.vel_y = 0
            self.on_ground = True

    def draw(self, surface, offset_x):
        if not self.alive:
            return
        draw_rect = pygame.Rect(self.rect)
        draw_rect.x -= offset_x
        pygame.draw.rect(surface, BROWN, draw_rect)
        circle_center = (draw_rect.x + self.width // 2, draw_rect.y)
        pygame.draw.circle(surface, YELLOW, circle_center, self.width // 2)


class Gate:
    def __init__(self, x, y, width=40, height=80, color=PURPLE):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface, offset_x):
        draw_rect = pygame.Rect(self.rect)
        draw_rect.x -= offset_x
        pygame.draw.rect(surface, self.color, draw_rect)
        inner_rect = pygame.Rect(draw_rect.x + 5, draw_rect.y + 10, self.width - 10, self.height - 20)
        pygame.draw.rect(surface, WHITE, inner_rect)


phases = [

    {
        "ground_platforms": [
            pygame.Rect(0, SCREEN_HEIGHT - 40, 400, 40),
            pygame.Rect(500, SCREEN_HEIGHT - 40, 400, 40),
            pygame.Rect(950, SCREEN_HEIGHT - 40, 400, 40),
            pygame.Rect(1400, SCREEN_HEIGHT - 40, 400, 40),
            pygame.Rect(1850, SCREEN_HEIGHT - 40, 350, 40),
        ],
        "other_platforms": [
            pygame.Rect(150, 450, 120, 20),
            pygame.Rect(350, 350, 120, 20),
            pygame.Rect(550, 250, 120, 20),
            pygame.Rect(750, 400, 120, 20),
            pygame.Rect(900, 300, 120, 20),
            pygame.Rect(1150, 350, 120, 20),
            pygame.Rect(1400, 250, 120, 20),
            pygame.Rect(1650, 450, 120, 20),
            pygame.Rect(1900, 350, 100, 20),
        ],
        "enemies_platform_indices": [1, 3, 6, 7],
        "enemies_speeds": [2, 1.5, 2.5, 3],
        "gate_start_pos": None,
        "gate_exit_pos": (2300, SCREEN_HEIGHT - 40 - 80),
        "gate_exit_color": PURPLE,
    },

    {
        "ground_platforms": [
            pygame.Rect(0, SCREEN_HEIGHT - 40, 300, 40),
            pygame.Rect(400, SCREEN_HEIGHT - 40, 300, 40),
            pygame.Rect(850, SCREEN_HEIGHT - 40, 400, 40),
            pygame.Rect(1300, SCREEN_HEIGHT - 40, 400, 40),
            pygame.Rect(1750, SCREEN_HEIGHT - 40, 400, 40),
            pygame.Rect(2200, SCREEN_HEIGHT - 40, 350, 40),
        ],
        "other_platforms": [
            pygame.Rect(100, 450, 100, 20),
            pygame.Rect(300, 350, 140, 20),
            pygame.Rect(550, 250, 140, 20),
            pygame.Rect(800, 400, 100, 20),
            pygame.Rect(1050, 300, 140, 20),
            pygame.Rect(1300, 250, 120, 20),
            pygame.Rect(1600, 450, 150, 20),
            pygame.Rect(1900, 350, 140, 20),
            pygame.Rect(2150, 300, 100, 20),
        ],
        "enemies_platform_indices": [1, 3, 5, 7],
        "enemies_speeds": [2.5, 1.7, 3, 2],
        "gate_start_pos": (10, SCREEN_HEIGHT - 40 - 80),
        "gate_start_color": ORANGE,
        "gate_exit_pos": (2600, SCREEN_HEIGHT - 40 - 80),
        "gate_exit_color": PURPLE,
    }
]

def load_phase(phase_index):
    phase_data = phases[phase_index]
    ground_platforms = phase_data["ground_platforms"]
    other_platforms = phase_data["other_platforms"]
    platforms = ground_platforms + other_platforms

    enemies = []
    for idx, spd in zip(phase_data["enemies_platform_indices"], phase_data["enemies_speeds"]):
        if idx < len(platforms):
            enemy = Enemy(platforms[idx], speed=spd)
            enemies.append(enemy)

    gate_start_pos = phase_data.get("gate_start_pos", None)
    gate_start_color = phase_data.get("gate_start_color", PURPLE)
    gate_exit_pos = phase_data["gate_exit_pos"]
    gate_exit_color = phase_data.get("gate_exit_color", PURPLE)

    gate_start = None
    if gate_start_pos is not None:
        gate_start = Gate(gate_start_pos[0], gate_start_pos[1], color=gate_start_color)
    gate_exit = Gate(gate_exit_pos[0], gate_exit_pos[1], color=gate_exit_color)

    return platforms, ground_platforms, other_platforms, enemies, gate_start, gate_exit

def start_screen():
    font_title = pygame.font.SysFont(None, 70)
    font_options = pygame.font.SysFont(None, 50)

    title_text = font_title.render("Platman Game", True, WHITE)
    play_text = font_options.render("Jogar", True, WHITE)
    exit_text = font_options.render("Sair", True, WHITE)

    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    play_rect = play_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
    exit_rect = exit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    return True
                if exit_rect.collidepoint(event.pos):
                    return False

        SCREEN.fill(BLUE)
        SCREEN.blit(title_text, title_rect)
        SCREEN.blit(play_text, play_rect)
        SCREEN.blit(exit_text, exit_rect)
        pygame.display.flip()
        CLOCK.tick(FPS)

def main():
    if not start_screen():
        pygame.quit()
        sys.exit()

    current_phase = 0
    platforms, ground_platforms, other_platforms, enemies, gate_start, gate_exit = load_phase(current_phase)

    player = Player()
    offset_x = 0

    font = pygame.font.SysFont(None, 30)

    game_won = False
    fading_in = False
    fade_start_time = 0

    running = True
    while running:
        dt = CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if player.alive and not game_won:
            dx = 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dx = -MOVE_SPEED
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx = MOVE_SPEED
            
            if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and player.on_ground:
                player.jump()
            player.update_jump(keys)

            player.move(dx, platforms)
            player.apply_gravity(platforms)

            if player.y > SCREEN_HEIGHT:
                player.alive = False

        else:
            if keys[pygame.K_r]:
                player = Player()
                offset_x = 0
                for enemy in enemies:
                    enemy.reset()
                player.alive = True
                if game_won:
                    current_phase = 0
                    platforms, ground_platforms, other_platforms, enemies, gate_start, gate_exit = load_phase(current_phase)
                    game_won = False
                fading_in = True
                fade_start_time = pygame.time.get_ticks()

        for enemy in enemies:
            enemy.update(platforms)

        if player.alive and not game_won:
            for enemy in enemies:
                if enemy.alive and player.rect.colliderect(enemy.rect):
                    if player.vel_y > 0 and player.rect.bottom - enemy.rect.top < 15:
                        enemy.alive = False
                        player.vel_y = -JUMP_SPEED / 1.5
                    else:
                        if player.rect.bottom > enemy.rect.top:
                            player.alive = False
                    break

        if gate_exit and player.rect.colliderect(gate_exit.rect):
            current_phase += 1
            if current_phase >= len(phases):
                game_won = True
                current_phase = len(phases) - 1
            else:
                platforms, ground_platforms, other_platforms, enemies, gate_start, gate_exit = load_phase(current_phase)
                player = Player()
                offset_x = 0
                fading_in = True
                fade_start_time = pygame.time.get_ticks()

        if gate_start and player.rect.colliderect(gate_start.rect):
            if current_phase > 0:
                current_phase -= 1
                platforms, ground_platforms, other_platforms, enemies, gate_start, gate_exit = load_phase(current_phase)
                player = Player()
                player.x = 2200.0 if current_phase == 0 else 0.0
                player.rect.x = int(player.x)
                offset_x = max(player.rect.x - SCREEN_WIDTH // 2, 0)
                fading_in = True
                fade_start_time = pygame.time.get_ticks()

        metade_tela = SCREEN_WIDTH // 2
        if player.rect.x - offset_x > metade_tela:
            offset_x = player.rect.x - metade_tela
        elif player.rect.x - offset_x < metade_tela and player.x > metade_tela:
            offset_x = player.rect.x - metade_tela
        if offset_x < 0:
            offset_x = 0

        SCREEN.fill(BLUE)

        for i, platform in enumerate(ground_platforms):
            draw_rect = pygame.Rect(platform)
            draw_rect.x -= offset_x
            color = DARK_GREEN if i % 2 == 0 else GREEN
            pygame.draw.rect(SCREEN, color, draw_rect)

        for i, platform in enumerate(other_platforms):
            draw_rect = pygame.Rect(platform)
            draw_rect.x -= offset_x
            color = GREEN if i % 2 == 0 else DARK_GREEN
            pygame.draw.rect(SCREEN, color, draw_rect)

        if gate_start:
            gate_start.draw(SCREEN, offset_x)

        if gate_exit:
            gate_exit.draw(SCREEN, offset_x)

        for enemy in enemies:
            enemy.draw(SCREEN, offset_x)

        if player.alive:
            player.draw(SCREEN, offset_x)

        phase_text = font.render(f"Fase: {current_phase + 1}", True, WHITE)
        SCREEN.blit(phase_text, (20, 40))

        if not player.alive:
            game_over_text = font.render("Você morreu! Pressione R para reiniciar.", True, WHITE)
            SCREEN.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                                        SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
        if game_won:
            win_text = font.render("Parabéns! Você venceu todas as fases! Pressione R para jogar novamente.", True, WHITE)
            SCREEN.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2,
                                  SCREEN_HEIGHT // 2 - win_text.get_height() // 2))
        if player.alive and not game_won:
            inst_text = font.render("Setas/A-D: mover, Espaço/W/Up: pular", True, WHITE)
            SCREEN.blit(inst_text, (20, 10))

        if fading_in:
            current_time = pygame.time.get_ticks()
            elapsed = current_time - fade_start_time
            if elapsed < FADE_IN_DURATION:
                fade_alpha = 255 - int(255 * (elapsed / FADE_IN_DURATION))
                fade_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                fade_surf.fill(BLACK)
                fade_surf.set_alpha(fade_alpha)
                SCREEN.blit(fade_surf, (0, 0))
            else:
                fading_in = False

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
