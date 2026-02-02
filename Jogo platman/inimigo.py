import pygame
import random
from config import GRAVITY, safe_load_sprite

class Enemy:
    def __init__(
        self,
        patrol_platform: pygame.Rect,
        speed=2,
        width=80,
        height=120,
        idle_paths=None,
        walk_paths=None,
        max_hp=1,
    ):
        self.patrol_platform = patrol_platform
        self.width = width
        self.height = height

        self.speed = speed
        self.direction = 1
        self.facing = 1

        self.vel_y = 0
        self.on_ground = False
        self.alive = True

        self.max_hp = max_hp
        self.hp = max_hp

        self.x = float(self.patrol_platform.left + 10)
        self.y = float(self.patrol_platform.top - self.height)
        self.rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)

        self.patrol_start = self.patrol_platform.left + 5
        self.patrol_end = self.patrol_platform.right - self.width - 5

        if idle_paths is None:
            idle_paths = ["sprites/lacaioR.png"]
        if walk_paths is None:
            walk_paths = ["sprites/lacaioR.png"]

        self.idle_sprites = [safe_load_sprite(p, (self.width, self.height)) for p in idle_paths]
        self.walk_sprites = [safe_load_sprite(p, (self.width, self.height)) for p in walk_paths]

        self.current_sprite = self.idle_sprites[0]
        self.moving = False
        self.walk_index = 0
        self.walk_counter = 0
        self.walk_speed = 8

    def reset(self):
        self.x = float(self.patrol_platform.left + 10)
        self.y = float(self.patrol_platform.top - self.height)
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        self.direction = 1
        self.facing = 1
        self.vel_y = 0
        self.on_ground = False
        self.alive = True
        self.hp = self.max_hp

        self.current_sprite = self.idle_sprites[0]
        self.walk_index = 0
        self.walk_counter = 0

    def take_damage(self, amount=1):
        if not self.alive:
            return
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.alive = False

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

    def update_animation(self):
        if not self.alive:
            return

        if not self.moving:
            self.current_sprite = self.idle_sprites[0]
            self.walk_counter = 0
            return

        self.walk_counter += 1
        if self.walk_counter >= self.walk_speed:
            self.walk_counter = 0
            self.walk_index = (self.walk_index + 1) % len(self.walk_sprites)

        self.current_sprite = self.walk_sprites[self.walk_index]

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

        self.facing = 1 if self.direction > 0 else -1
        self.moving = True

        self.apply_gravity(platforms)

        if self.rect.bottom > self.patrol_platform.top:
            self.rect.bottom = self.patrol_platform.top
            self.y = self.rect.y
            self.vel_y = 0
            self.on_ground = True

        self.update_animation()

    def draw(self, surface, offset_x):
        if not self.alive:
            return

        draw_rect = pygame.Rect(self.rect)
        draw_rect.x -= offset_x
        
        sprite = self.current_sprite
        if self.facing < 0:
            sprite = pygame.transform.flip(sprite, True, False)

        surface.blit(sprite, (draw_rect.x, draw_rect.y))

        bar_w = self.rect.w
        bar_h = 10
        px = draw_rect.x
        py = draw_rect.y +14

        pygame.draw.rect(surface, (60, 60, 60), (px, py, bar_w, bar_h))
        vida_w = int(bar_w * max(0, self.hp) / self.max_hp)
        pygame.draw.rect(surface, (0, 200, 0), (px, py, vida_w, bar_h))


class Boss(Enemy):
    def __init__(self, patrol_platform, speed=2):
        super().__init__(
            patrol_platform=patrol_platform,
            speed=speed,
            width=80,
            height=80,
            max_hp=20,
        )

        self.x = float(self.patrol_platform.left + 500)
        self.y = float(self.patrol_platform.top - self.height)

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        self.hp = 20
        self.max_hp = 20

        self.facing = 1
        self.moving = False

        self.idle_sprites = [
            safe_load_sprite("sprites/bossD.png", (self.width, self.height)),
        ]

        self.walk_sprites = [
            safe_load_sprite("sprites/ando1.png", (self.width - 22, self.height - 22)),
            safe_load_sprite("sprites/ando2.png", (self.width - 22, self.height - 22)),
            safe_load_sprite("sprites/ando3.png", (self.width - 22, self.height - 22)),
        ]

        self.current_sprite = self.idle_sprites[0]
        self.walk_index = 0
        self.walk_counter = 0
        self.walk_speed = 8

        self._ai_timer = 0
        self._ai_interval = 30
        self.sprite_offset_y = 20
        


    def update(self, platforms):
        if not self.alive:
            return

        self._ai_timer += 1
        if self._ai_timer >= self._ai_interval:
            self._ai_timer = 0
            self._ai_interval = random.randint(20, 50)
            if random.random() < 0.5:
                self.direction *= -1
            if self.on_ground and random.random() < 0.35:
                self.vel_y = -12

        super().update(platforms)
    def draw(self, surface, offset_x):
        if not self.alive:
            return

        draw_rect = pygame.Rect(self.rect)
        draw_rect.x -= offset_x
        
        sprite = self.current_sprite
        if self.facing < 0:
            sprite = pygame.transform.flip(sprite, True, False)

        surface.blit(sprite, (draw_rect.x, draw_rect.y+20))

        bar_w = self.rect.w
        bar_h = 10
        px = draw_rect.x
        py = draw_rect.y - 14 + 20

        pygame.draw.rect(surface, (60, 60, 60), (px, py, bar_w, bar_h))
        vida_w = int(bar_w * max(0, self.hp) / self.max_hp)
        pygame.draw.rect(surface, (0, 200, 0), (px, py, vida_w, bar_h))

    
