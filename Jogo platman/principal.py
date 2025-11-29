# principal.py
import pygame
import sys
from config import *
from player import Player
from fases import load_phase
from plataformas import get_platform_texture
from inimigo import Enemy  # (opcionalmente usado por load_phase)
from portao import Gate    # (opcionalmente usado por load_phase)

def start_screen():
    play_music(INTRO_MUSIC, loops=-1)
    try:
        pygame.mixer.music.set_volume(0.3)
    except Exception:
        pass
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

    play_music(GAME_MUSIC, loops=-1)
    try:
        pygame.mixer.music.set_volume(0.3)
    except Exception:
        pass

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
            player.moving = False
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dx = -MOVE_SPEED
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx = MOVE_SPEED
            if dx != 0:
                player.moving = True

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
                try:
                    som_reset.play()
                except Exception:
                    pass
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
            if current_phase >= len(__import__("fases").fases):
                game_won = True
                current_phase = len(__import__("fases").fases) - 1
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

        # --- desenhar ground platforms ---
        for platform in ground_platforms:
            draw_rect = pygame.Rect(platform)
            draw_rect.x -= offset_x
            tex = get_platform_texture(draw_rect.width, draw_rect.height)
            SCREEN.blit(tex, (draw_rect.x, draw_rect.y))

        # --- desenhar other platforms ---
        for platform in other_platforms:
            draw_rect = pygame.Rect(platform)
            draw_rect.x -= offset_x
            tex = get_platform_texture(draw_rect.width, draw_rect.height)
            SCREEN.blit(tex, (draw_rect.x, draw_rect.y))

        if gate_start:
            gate_start.draw(SCREEN, offset_x)

        if gate_exit:
            gate_exit.draw(SCREEN, offset_x)

        for enemy in enemies:
            enemy.draw(SCREEN, offset_x)

        # --- atualizar animação do jogador ---
        player.update_animation(dt)

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

    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
