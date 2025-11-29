# player.py
import pygame
from config import (
    PLATMAN_WIDTH, PLATMAN_HEIGHT, JUMP_SPEED, GRAVITY,
    MAX_JUMP_TIME, MAX_JUMP_HEIGHT, PLAYER_ANIM_INTERVAL_MS,
    SPRITE_PATHS, safe_load_sprite
)

class Player:
    def __init__(self):
        self.x = 100.0
        self.y = 600 - PLATMAN_HEIGHT - 50
        self.rect = pygame.Rect(int(self.x), int(self.y), PLATMAN_WIDTH, PLATMAN_HEIGHT)
        self.vel_y = 0
        self.on_ground = False
        self.alive = True
        self.jump_time = 0

        self.sprites = [safe_load_sprite(p, (PLATMAN_WIDTH, PLATMAN_HEIGHT)) for p in SPRITE_PATHS]

        self.frame = 0
        self.anim_timer = 0.0
        self.anim_interval = PLAYER_ANIM_INTERVAL_MS
        self.facing = 1
        self.moving = False

        self.idle_frame = 0
        if len(self.sprites) >= 3:
            self.jump_frame = len(self.sprites) - 1
            self.walk_frames = list(range(1, len(self.sprites) - 1))
        else:
            self.jump_frame = None if len(self.sprites) < 3 else len(self.sprites) - 1
            self.walk_frames = [i for i in range(1, len(self.sprites))]

        if not self.walk_frames:
            self.walk_frames = [self.idle_frame]

        self.walk_index = 0

    def move(self, dx, platforms):
        if dx > 0:
            self.facing = 1
        elif dx < 0:
            self.facing = -1

        self.x += dx
        if self.x < 0:
            self.x = 0
        self.rect.x = int(self.x)

        for platform in platforms:
            if self.rect.colliderect(platform):
                if dx > 0:
                    self.rect.right = platform.left
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
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = platform.bottom
                    self.vel_y = 0
                self.y = self.rect.y

    def jump(self):
        if self.on_ground:
            self.jump_time = 0
            self.vel_y = -JUMP_SPEED
            try:
                # som_pulo é definido em config
                from config import som_pulo
                som_pulo.play()
            except Exception:
                pass

    def update_jump(self, keys):
        if keys[pygame.K_SPACE] or keys[pygame.K_w]:
            if self.jump_time < MAX_JUMP_TIME:
                self.jump_time += 1
                self.vel_y = -JUMP_SPEED * (1 + self.jump_time / MAX_JUMP_TIME)
                if self.rect.y <= 600 - PLATMAN_HEIGHT - MAX_JUMP_HEIGHT:
                    self.vel_y = -JUMP_SPEED
        else:
            self.jump_time = MAX_JUMP_TIME

    def update_animation(self, dt):
        if not self.on_ground:
            if self.jump_frame is not None:
                self.frame = self.jump_frame
            else:
                self.frame = self.idle_frame
            self.anim_timer = 0
            self.walk_index = 0
            return

        if not self.moving:
            self.frame = self.idle_frame
            self.anim_timer = 0
            self.walk_index = 0
            return

        if len(self.walk_frames) == 1:
            self.frame = self.walk_frames[0]
            return

        self.anim_timer += dt
        while self.anim_timer >= self.anim_interval:
            self.anim_timer -= self.anim_interval
            self.walk_index = (self.walk_index + 1) % len(self.walk_frames)

        self.frame = self.walk_frames[self.walk_index]

    def draw(self, surface, offset_x):
        draw_rect = pygame.Rect(self.rect)
        draw_rect.x -= offset_x

        sprite = self.sprites[self.frame]
        if self.facing < 0:
            sprite = pygame.transform.flip(sprite, True, False)

        surface.blit(sprite, (draw_rect.x, draw_rect.y))
