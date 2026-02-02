import pygame
from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WHITE,
    BLUE,
    CLOCK,
    FPS,
    SCREEN,
    INTRO_MUSIC,
    play_music
)

menu_bg = pygame.image.load("sprites/cenarioinicial.png").convert()
menu_bg = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))


def start_screen():
    play_music(INTRO_MUSIC, loops=-1)

    PIXEL_SCALE = 3
    UI_PURPLE = (200, 0, 255) 

    def render_pixel_text(text, base_size):
        f = pygame.font.SysFont(None, base_size)
        s = f.render(text, False, UI_PURPLE) 
        return pygame.transform.scale(s, (s.get_width() * PIXEL_SCALE, s.get_height() * PIXEL_SCALE))

    def draw_pixel_button(surface, rect, text_surf, hovered=False):
        fill = (40, 0, 60) if not hovered else (70, 0, 100)
        border = UI_PURPLE
        inner = (120, 0, 160)

        pygame.draw.rect(surface, fill, rect)
        pygame.draw.rect(surface, border, rect, 5)
        inner_rect = rect.inflate(-10, -10)
        pygame.draw.rect(surface, inner, inner_rect, 2)

        text_rect = text_surf.get_rect(center=rect.center)
        surface.blit(text_surf, text_rect)

    play_surf = render_pixel_text("JOGAR", base_size=18)
    exit_surf = render_pixel_text("SAIR", base_size=18)

    btn_w, btn_h = 260, 80
    play_btn = pygame.Rect(0, 0, btn_w, btn_h)
    exit_btn = pygame.Rect(0, 0, btn_w, btn_h)
    play_btn.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)
    exit_btn.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 140)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        hover_play = play_btn.collidepoint(mouse_pos)
        hover_exit = exit_btn.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.collidepoint(event.pos):
                    return True
                if exit_btn.collidepoint(event.pos):
                    return False

        SCREEN.blit(menu_bg, (0, 0))

        draw_pixel_button(SCREEN, play_btn, play_surf, hovered=hover_play)
        draw_pixel_button(SCREEN, exit_btn, exit_surf, hovered=hover_exit)

        pygame.display.flip()
        CLOCK.tick(FPS)
