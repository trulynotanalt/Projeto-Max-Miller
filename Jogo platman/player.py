import pygame
from config import (
    PLATMAN_WIDTH, PLATMAN_HEIGHT,
    MIN_WORLD_X,
    LEFT_WALL_X, LEFT_WALL_OPEN_Y,
    JUMP_SPEED, GRAVITY,
    MAX_JUMP_TIME, MAX_JUMP_HEIGHT,
    safe_load_sprite
)

class Player:
    def __init__(self):
        self.x = 1940.0
        self.y = 600 - PLATMAN_HEIGHT - 50
        self.hitbox = pygame.Rect(int(self.x), int(self.y), PLATMAN_WIDTH, PLATMAN_HEIGHT)
        self.rect = pygame.Rect(int(self.x), int(self.y), PLATMAN_WIDTH, PLATMAN_HEIGHT)

        self.vel_y = 0
        self.on_ground = False
        self.alive = True
        self.jump_time = 0
        self.tem_pulo_duplo = False
        self.usou_pulo_duplo = False

        

        self.facing = 1
        self.moving = False

        self.idle_sprites = [
            safe_load_sprite("sprites/sprite_0.png", (PLATMAN_WIDTH, PLATMAN_HEIGHT))
        ]

        self.walk_sprites = [
            safe_load_sprite("sprites/sprite_1.png", (PLATMAN_WIDTH, PLATMAN_HEIGHT)),
            safe_load_sprite("sprites/sprite_2.png", (PLATMAN_WIDTH, PLATMAN_HEIGHT)),
        ]

        self.current_sprite = self.idle_sprites[0]
        self.walk_index = 0
        self.walk_counter = 0
        self.walk_speed = 6

    def move(self, dx, platforms):
        prev_rect = pygame.Rect(self.rect)
        self.moving = dx != 0

        if dx > 0:
            self.facing = 1
        elif dx < 0:
            self.facing = -1

        self.x += dx
        if self.x < MIN_WORLD_X:
            self.x = MIN_WORLD_X
        self.rect.x = int(self.x)

       
        if self.rect.top > LEFT_WALL_OPEN_Y:
            if dx < 0 and self.rect.left < LEFT_WALL_X:
                self.rect.left = LEFT_WALL_X
                self.x = self.rect.x

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
                    self.usou_pulo_duplo = False
                    self.y = self.rect.y

                
    
    def pulo_duplo(self):
        if self.tem_pulo_duplo:
            self.vel_y = -JUMP_SPEED * 1.3
            self.usou_pulo_duplo = True


    def jump(self):
        if self.on_ground:
            self.jump_time = 0
            self.vel_y = -JUMP_SPEED
            try:
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

    def update_animation(self,dt):
        if not self.moving:
            self.current_sprite = self.idle_sprites[0]
            self.walk_counter = 0
            return

        self.walk_counter += 1
        if self.walk_counter >= self.walk_speed:
            self.walk_counter = 0
            self.walk_index = (self.walk_index + 1) % len(self.walk_sprites)

        self.current_sprite = self.walk_sprites[self.walk_index]

    @property
    def facing_right(self):
        return self.facing >= 0

    def draw(self, surface, offset_x):
        draw_rect = pygame.Rect(self.rect)
        draw_rect.x -= offset_x

        sprite = self.current_sprite
        if self.facing < 0:
            sprite = pygame.transform.flip(sprite, True, False)

        surface.blit(sprite, (draw_rect.x, draw_rect.y))
