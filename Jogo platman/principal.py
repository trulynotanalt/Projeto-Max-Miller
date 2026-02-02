
import pygame
import sys
from config import *
from player import Player
from fases import load_phase
from plataformas import *
from inimigo import Enemy 
from portao import Gate    
from voz_comando import start_voice_listener, should_quit, consume_start, consume_restart, request_quit
from pulo import Pulo


PHASE2_MUSIC = "sons_musicas/bossmusica.mp3"
pygame.mixer.music.set_volume(0.4)


class Bullet:
    _base_image = None
    def __init__(self, x, y, direction):
        if Bullet._base_image is None:
            Bullet._base_image = safe_load_sprite(BULLET_SPRITE, BULLET_SIZE)
        self.image = Bullet._base_image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = BULLET_SPEED * direction

    def update(self):
        self.rect.x += self.speed

    def draw(self, screen, offset_x):
        screen.blit(self.image, (self.rect.x - offset_x, self.rect.y))


menu_bg = pygame.image.load("sprites/cenarioinicial.png").convert()
menu_bg = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
GAME_BG_PATH = "sprites/salajogo.jpg"  
game_bg = safe_load_sprite(GAME_BG_PATH, (SCREEN_WIDTH, SCREEN_HEIGHT))



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
      
        if should_quit():
            return False
        if consume_start():
            return True

        mouse_pos = pygame.mouse.get_pos()
        hover_play = play_btn.collidepoint(mouse_pos)
        hover_exit = exit_btn.collidepoint(mouse_pos)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                request_quit()
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
        
        
def main():
    
    start_voice_listener(language="pt-BR")

    
    game_start_tick = pygame.time.get_ticks()

    if not start_screen():
        pygame.quit()
        sys.exit()

    play_music(GAME_MUSIC, loops=-1)
    try:
        pygame.mixer.music.set_volume(0.3)
    except Exception:
        pass

    current_phase = 0
    platforms, ground_platforms, other_platforms, enemies, gate_start, gate_exit,boss, pulos, platwoman = load_phase(current_phase)



    player = Player()
    
    player_has_gun = False
    bullets = []

   
    SHOT_COOLDOWN_MS = 6000  
    last_shot_ms = -999999



    
    gun_rect = None
    gun_image = None

    def spawn_gun_for_phase():
        
        nonlocal gun_rect, gun_image
        if player_has_gun:
            gun_rect = None
            gun_image = None
            return

        phase_data = __import__("fases").phases[current_phase]
        gun_pos = phase_data.get("gun_pos", None)
        if gun_pos is None:
            gun_rect = None
            gun_image = None
            return

        gx, gy = gun_pos
        gun_image = safe_load_sprite(GUN_SPRITE, GUN_SIZE)  
        gun_rect = gun_image.get_rect(topleft=(gx, gy))


    def on_player_death():
        
        nonlocal player_has_gun, bullets
        player_has_gun = False
        bullets.clear()
        spawn_gun_for_phase()


    spawn_gun_for_phase()

    offset_x = 0
    font = pygame.font.SysFont(None, 30)


    
    UI_PURPLE_LIGHT = (220, 130, 255) 
    PIXEL_UI_SCALE = 2                

    def render_ui_text(msg: str, base_size: int = 18):
        f = pygame.font.SysFont(None, base_size)
        s = f.render(msg, False, UI_PURPLE_LIGHT) 
        return pygame.transform.scale(s, (s.get_width() * PIXEL_UI_SCALE, s.get_height() * PIXEL_UI_SCALE))

    def draw_pixel_button(surface, rect, text_surf, hovered=False):
        fill = (40, 0, 60) if not hovered else (70, 0, 100)
        border = UI_PURPLE_LIGHT
        inner = (120, 0, 160)
        pygame.draw.rect(surface, fill, rect)
        pygame.draw.rect(surface, border, rect, 5)
        inner_rect = rect.inflate(-10, -10)
        pygame.draw.rect(surface, inner, inner_rect, 2)
        surface.blit(text_surf, text_surf.get_rect(center=rect.center))

    def format_time(ms: int) -> str:
        total_s = max(0, ms // 1000)
        m = total_s // 60
        s = total_s % 60
        return f"{m:02d}:{s:02d}"

    
    paused = False
    pause_start_real = 0
    paused_total_ms = 0
    pause_snapshot = None
    pause_msg = ""


    def game_ticks() -> int:
        
        return pygame.time.get_ticks() - paused_total_ms

    
    life_start_tick = game_ticks()
    last_life_time_ms = 0

    
    btn_w, btn_h = 280, 80
    restart_btn = pygame.Rect(0, 0, btn_w, btn_h)
    exit_btn = pygame.Rect(0, 0, btn_w, btn_h)
    restart_btn.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90)
    exit_btn.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 190)

    restart_surf = render_ui_text("REINICIAR", base_size=18)

   
    continue_btn = pygame.Rect(0, 0, btn_w, btn_h)
    continue_btn.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10)
    continue_surf = render_ui_text("CONTINUAR", base_size=18)
    exit_surf = render_ui_text("SAIR", base_size=18)

    game_won = False
    fading_in = False
    fade_start_time = 0
    def set_music_for_phase(phase_idx: int):
       
        if phase_idx == 1:
            play_music(PHASE2_MUSIC, loops=-1)
        else:
            play_music(GAME_MUSIC, loops=-1)
        try:
            pygame.mixer.music.set_volume(0.3)
        except Exception:
            pass

    def do_reset():
        nonlocal current_phase
        nonlocal platforms, ground_platforms, other_platforms, enemies, gate_start, gate_exit,boss, pulos, platwoman
        nonlocal player, offset_x, game_won, fading_in, fade_start_time, life_start_tick, last_life_time_ms
        nonlocal player_has_gun, bullets, gun_rect, gun_image

        player = Player()
        offset_x = 0

        player.tem_pulo_duplo = False
        player.usou_pulo_duplo = False
        


       
        player_has_gun = False
        bullets.clear()
        spawn_gun_for_phase()

        
        life_start_tick = game_ticks()
        last_life_time_ms = 0

        try:
            som_reset.play()
        except Exception:
            pass

        for enemy in enemies:
            try:
                enemy.reset()
            except Exception:
                pass
        
        


        player.alive = True

        if game_won:
            current_phase = 0
            platforms, ground_platforms, other_platforms, enemies, gate_start, gate_exit,boss, pulos, platwoman = load_phase(current_phase)

            spawn_gun_for_phase()
            game_won = False

        fading_in = True
        fade_start_time = game_ticks()


    running = True
    while running:
        
        if should_quit():
            running = False
            break
       
        if consume_restart() and (not player.alive or game_won):
            do_reset()
            continue

        dt = CLOCK.tick(FPS)
        did_reset = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                request_quit()
                running = False
                break


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player.on_ground:
                        player.jump()
                    else:
                        player.pulo_duplo()
               
                if event.key == pygame.K_g and player.alive and not game_won:
                    if not paused:
                        paused = True
                        pause_start_real = pygame.time.get_ticks()
                        pause_snapshot = SCREEN.copy()  
                    else:
                        paused = False
                        pause_msg = ""
                        paused_total_ms += pygame.time.get_ticks() - pause_start_real

                    continue

                if event.key == pygame.K_f and player_has_gun and player.alive and not game_won and not paused:
                    now_ms = game_ticks()
                    if now_ms - last_shot_ms >= SHOT_COOLDOWN_MS:
                        last_shot_ms = now_ms
                        bullets.append(
                            Bullet(
                                player.rect.centerx,
                                player.rect.centery,
                                player.facing
                            )
                        )
                        try:
                            som_tiro.play()
                        except Exception:
                            pass


            if event.type == pygame.MOUSEBUTTONDOWN:
                if paused:
                    if continue_btn.collidepoint(event.pos):
                        
                        paused = False
                        pause_msg = ""
                        paused_total_ms += pygame.time.get_ticks() - pause_start_real

                    elif restart_btn.collidepoint(event.pos):
                        paused = False
                        paused_total_ms += pygame.time.get_ticks() - pause_start_real
                        do_reset()
                        did_reset = True
                        break
                    elif exit_btn.collidepoint(event.pos):
                        request_quit()
                        running = False
                        break

                if (not player.alive or game_won):
                    if restart_btn.collidepoint(event.pos):
                        do_reset()
                        did_reset = True
                        break
                    if exit_btn.collidepoint(event.pos):
                        request_quit()
                        running = False
                        break
        
        if not running:
            break
        if did_reset:
            continue

        
        if paused:
            if pause_snapshot is not None:
                SCREEN.blit(pause_snapshot, (0, 0))
            else:
                SCREEN.blit(game_bg, (0, 0))

            pause_surf = render_ui_text("JOGO PAUSADO", base_size=22)
            pause_rect = pause_surf.get_rect(midbottom=(SCREEN_WIDTH // 2, continue_btn.top - 20))
            SCREEN.blit(pause_surf, pause_rect)
            if pause_msg:
                msg_surf = render_ui_text(pause_msg, base_size=16)
                SCREEN.blit(msg_surf, (SCREEN_WIDTH // 2 - msg_surf.get_width() // 2, pause_rect.bottom + 10))


            mouse_pos = pygame.mouse.get_pos()
            draw_pixel_button(SCREEN, continue_btn, continue_surf, hovered=continue_btn.collidepoint(mouse_pos))
            draw_pixel_button(SCREEN, restart_btn, restart_surf, hovered=restart_btn.collidepoint(mouse_pos))
            draw_pixel_button(SCREEN, exit_btn, exit_surf, hovered=exit_btn.collidepoint(mouse_pos))

            hint_surf = render_ui_text("G: CONTINUAR", base_size=14)
            SCREEN.blit(hint_surf, (20, 40))

            pygame.display.flip()
            continue

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
            
            if gun_rect and player.rect.colliderect(gun_rect):
                player_has_gun = True
                gun_rect = None
                gun_image = None
                try:
                    som_pegar_arma.play()
                except Exception:
                    pass

            if player.y > SCREEN_HEIGHT:
                player.alive = False
                last_life_time_ms = game_ticks() - life_start_tick
                on_player_death()
        else:
            if keys[pygame.K_r]:
                do_reset()

        for enemy in enemies:
            enemy.update(platforms)
        if boss is not None and boss.alive and not game_won:
             boss.update(platforms)

        
        for pl in pulos:
            if pl.active and player.rect.colliderect(pl.rect):
                pl.active = False
                player.tem_pulo_duplo = True



        if player.alive and not game_won:
            for enemy in enemies:
                if enemy.alive and player.rect.colliderect(enemy.rect):
                    if player.vel_y > 0 and player.rect.bottom - enemy.rect.top < 15:
                        enemy.take_damage(1)
                        kill = pygame.mixer.Sound("sons_musicas/morte_inimigo.mp3")
                        kill.set_volume(0.3)
                        kill.play()
                        player.vel_y = -JUMP_SPEED / 1.5
                    else:
                        if player.rect.bottom > enemy.rect.top:
                            player.alive = False
                            last_life_time_ms = game_ticks() - life_start_tick
                            on_player_death()
                    break
        if player.alive and not game_won and boss is not None and boss.alive:
            if player.rect.colliderect(boss.rect):
                if player.vel_y > 0 and (player.rect.bottom - boss.rect.top) < 15:
                    boss.take_damage(1)
                    player.vel_y = -JUMP_SPEED / 1.3
                else:
                    player.alive = False
                    last_life_time_ms = game_ticks() - life_start_tick
                    on_player_death()

        if not game_won and boss is not None and (not boss.alive or boss.hp <= 0):
            game_won = True
        if player.alive and not game_won and gate_start and player.rect.colliderect(gate_start.rect):
            if current_phase > 0:
                current_phase -= 1
                platforms, ground_platforms, other_platforms, enemies, gate_start, gate_exit, boss, pulos, platwoman = load_phase(current_phase)

                set_music_for_phase(current_phase)

                bullets.clear()
                spawn_gun_for_phase()

                player = Player()
                player.x = 1940.0 if current_phase == 0 else 0.0
                player.y = 600 - player.rect.height - 50
                player.rect.x = int(player.x)
                player.rect.y = int(player.y)

                offset_x = max(player.rect.x - SCREEN_WIDTH // 2, 0)
                fading_in = True
                fade_start_time = game_ticks()


            

    

        

        
        if player.alive and not game_won and gate_exit and player.rect.colliderect(gate_exit.rect):
            current_phase += 1

            if current_phase >= len(__import__("fases").phases):
                game_won = True
                current_phase = len(__import__("fases").phases) - 1
            else:
                platforms, ground_platforms, other_platforms, enemies, gate_start, gate_exit,boss, pulos, platwoman = load_phase(current_phase)


                set_music_for_phase(current_phase)

                bullets.clear()
                spawn_gun_for_phase()

                player = Player()
                player.x = 100.0
                player.y = 600 - player.rect.height - 50
                player.rect.x = int(player.x)
                player.rect.y = int(player.y)

                offset_x = 0
                fading_in = True
                fade_start_time = game_ticks()



        
        metade_tela = SCREEN_WIDTH // 2
        if player.rect.x - offset_x > metade_tela:
            offset_x = player.rect.x - metade_tela
        elif player.rect.x - offset_x < metade_tela and player.x > metade_tela:
            offset_x = player.rect.x - metade_tela

        
        if player.rect.left < 0:
            offset_x = max(player.rect.x - metade_tela, MIN_OFFSET_X)
       
        if player.rect.left >= 0 and offset_x < 0:
            offset_x = 0
        if player.rect.left < 0 and offset_x < MIN_OFFSET_X:
            offset_x = MIN_OFFSET_X

        
        if current_phase == 1:
            GAME_BG_PATH = "sprites/salaboss.jpg"
            game_bg = safe_load_sprite(GAME_BG_PATH, (SCREEN_WIDTH, SCREEN_HEIGHT))
            SCREEN.blit(game_bg, (0, 0))
           
        else:
            GAME_BG_PATH = "sprites/salajogo.jpg"
            game_bg = safe_load_sprite(GAME_BG_PATH, (SCREEN_WIDTH, SCREEN_HEIGHT))
            SCREEN.blit(game_bg, (0, 0))
            

        
        
        for bullet in bullets[:]:
            bullet.update()

           
            if bullet.rect.x < -500 or bullet.rect.x > 5000:
                bullets.remove(bullet)
                continue

            hit = False

           
            if bullet.rect.left < LEFT_WALL_X and bullet.rect.top > LEFT_WALL_OPEN_Y:
                hit = True

            
            if not hit:
                for p in platforms:
                    if bullet.rect.colliderect(p):
                        hit = True
                        break

           
            

           
            if not hit and gate_start and bullet.rect.colliderect(gate_start.rect):
                hit = True
            if not hit and gate_exit and bullet.rect.colliderect(gate_exit.rect):
                hit = True

            
            if not hit and boss is not None and boss.alive and bullet.rect.colliderect(boss.rect):
                boss.take_damage(boss.hp)  # mata na hora
                hit = True

            if not hit:
                for enemy in enemies:
                    if enemy.alive and bullet.rect.colliderect(enemy.rect):
                        hit = True
                        break
            

            if hit:
                bullets.remove(bullet)


        for i, item in enumerate(ground_platforms):
            rect, inf_x, inf_y, extra_w, extra_h, img_off_x, img_off_y = item
            draw_rect = pygame.Rect(rect)
            draw_rect.x -= offset_x
            tex = get_platform_texture(draw_rect.width, draw_rect.height, extra_w=extra_w, extra_h=extra_h)
            SCREEN.blit(tex, (draw_rect.x + img_off_x, draw_rect.y + img_off_y))

        for i, item in enumerate(other_platforms):
            rect, inf_x, inf_y, extra_w, extra_h, img_off_x, img_off_y = item
            draw_rect = pygame.Rect(rect)
            draw_rect.x -= offset_x

            
            if rect.x < 0:
                if rect.y >= 150:
                    pygame.draw.rect(SCREEN, BLACK, draw_rect)
                continue

            tex = get_platform_texture(draw_rect.width, draw_rect.height, extra_w=extra_w, extra_h=extra_h)
            SCREEN.blit(tex, (draw_rect.x + img_off_x, draw_rect.y + img_off_y))

        
        for pl in pulos:
            pl.draw(SCREEN, offset_x)
        for pw in platwoman:
            pw.draw(SCREEN, offset_x)
        

        
        if gun_rect and gun_image:
            SCREEN.blit(gun_image, (gun_rect.x - offset_x, gun_rect.y))

        for bullet in bullets:
            bullet.draw(SCREEN, offset_x)





       
        if gate_start:
            gate_start.draw(SCREEN, offset_x)
        if gate_exit:
            gate_exit.draw(SCREEN, offset_x)
        for enemy in enemies:
            enemy.draw(SCREEN, offset_x)
        if boss is not None:
            boss.draw(SCREEN, offset_x)

        

       
        player.update_animation(dt)
        if player.alive:
            player.draw(SCREEN, offset_x)
        
        now = game_ticks()

        
        phase_surf = render_ui_text(f"FASE: {current_phase + 1}", base_size=16)
        SCREEN.blit(phase_surf, (20, 40))

        total_time_ms = now - game_start_tick
        total_surf = render_ui_text(f"TEMPO TOTAL: {format_time(total_time_ms)}", base_size=14)
        SCREEN.blit(total_surf, (20, 70))

        
        if player.alive and not game_won:
            alive_ms = now - life_start_tick
            alive_surf = render_ui_text(f"TEMPO VIVO: {format_time(alive_ms)}", base_size=14)
            SCREEN.blit(alive_surf, (20, 100))

            inst_surf = render_ui_text("SETAS/A-D: mover  |  ESPAÇO/W: pular", base_size=14)
            SCREEN.blit(inst_surf, (20, 10))

        if not player.alive:
            if last_life_time_ms == 0:
                last_life_time_ms = now - life_start_tick

            title_surf = render_ui_text("VOCE MORREU!", base_size=22)
            SCREEN.blit(title_surf, (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, SCREEN_HEIGHT // 2 - 160))

            alive_surf = render_ui_text(f"TEMPO VIVO: {format_time(last_life_time_ms)}", base_size=18)
            SCREEN.blit(alive_surf, (SCREEN_WIDTH // 2 - alive_surf.get_width() // 2, SCREEN_HEIGHT // 2 - 110))

            total_surf_center = render_ui_text(f"TEMPO TOTAL: {format_time(total_time_ms)}", base_size=16)
            SCREEN.blit(total_surf_center, (SCREEN_WIDTH // 2 - total_surf_center.get_width() // 2, SCREEN_HEIGHT // 2 - 70))

            mouse_pos = pygame.mouse.get_pos()
            draw_pixel_button(SCREEN, restart_btn, restart_surf, hovered=restart_btn.collidepoint(mouse_pos))
            draw_pixel_button(SCREEN, exit_btn, exit_surf, hovered=exit_btn.collidepoint(mouse_pos))

        if game_won:
            title_surf = render_ui_text("VOCE VENCEU!", base_size=22)
            SCREEN.blit(title_surf, (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, SCREEN_HEIGHT // 2 - 160))

            total_surf_center = render_ui_text(f"TEMPO TOTAL: {format_time(total_time_ms)}", base_size=18)
            SCREEN.blit(total_surf_center, (SCREEN_WIDTH // 2 - total_surf_center.get_width() // 2, SCREEN_HEIGHT // 2 - 110))

            ms_secreta = render_ui_text("O começo depois do fim ", base_size=22)
            SCREEN.blit(ms_secreta, (SCREEN_WIDTH // 2 - ms_secreta.get_width() // 2, SCREEN_HEIGHT // 2 - 35))


            mouse_pos = pygame.mouse.get_pos()
            draw_pixel_button(SCREEN, restart_btn, restart_surf, hovered=restart_btn.collidepoint(mouse_pos))
            draw_pixel_button(SCREEN, exit_btn, exit_surf, hovered=exit_btn.collidepoint(mouse_pos))

      
        if fading_in:
            current_time = game_ticks()
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
