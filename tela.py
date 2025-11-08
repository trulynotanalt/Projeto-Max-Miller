import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLUE, CLOCK, FPS, SCREEN

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
