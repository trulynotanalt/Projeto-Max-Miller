# inimigo.py
import pygame
from config import GRAVITY, BROWN, YELLOW

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
