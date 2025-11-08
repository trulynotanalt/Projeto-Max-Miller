import pygame
from config import SCREEN_HEIGHT, PLATMAN_WIDTH, PLATMAN_HEIGHT, MOVE_SPEED, JUMP_SPEED, GRAVITY, MAX_JUMP_TIME, MAX_JUMP_HEIGHT, WHITE, SKIN, BLACK

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
