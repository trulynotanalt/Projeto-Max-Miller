import pygame
from inimigo import Enemy, Boss
from portao import Gate
from config import SCREEN_HEIGHT, PURPLE, ORANGE, PORTAL_START_SPRITE, PORTAL_EXIT_SPRITE, PORTAL_START_SPRITE_SIZE, PORTAL_EXIT_SPRITE_SIZE, PORTAL_START_SPRITE_OFFSET, PORTAL_EXIT_SPRITE_OFFSET
from espinho import RectVermelho
from pulo import RectAzul



# (
#     pygame.Rect(0, SCREEN_HEIGHT - 40, 150, 40),  
#     # rect_base → posição e tamanho LÓGICO da plataforma
#     # x = 0
#     # y = SCREEN_HEIGHT - 40
#     # largura = 150
#     # altura = 40
#     # serve como base para desenho, colisão e inimigos

#     -90,  
#     # inf_x → ajuste da HITBOX no eixo X
#     # valor negativo DIMINUI a largura da colisão
#     # -90 = remove 90px da largura total (45px de cada lado)

#     -1,   
#     # inf_y → ajuste da HITBOX no eixo Y
#     # -1 diminui levemente a altura da colisão
#     # ajuda a evitar bugs de colisão no topo

#     0,    
#     # extra_w → aumento da LARGURA da IMAGEM
#     # NÃO afeta colisão
#     # 0 = imagem com mesma largura do rect_base

#     30,   
#     # extra_h → aumento da ALTURA da IMAGEM
#     # NÃO afeta colisão
#     # usado para sprites mais altos (chão mais grosso)

#     0,    
#     # img_off_x → deslocamento da IMAGEM no eixo X
#     # positivo = direita | negativo = esquerda
#     # 0 = imagem alinhada horizontalmente ao rect

#     30,   
#     # img_off_y → deslocamento da IMAGEM no eixo Y
#     # positivo = desce | negativo = sobe
#     # usado para compensar o extra_h e manter a imagem no chão
# )

hit_other_x = -75
hit_ground_x = -180

phases = [
    {
        "ground_platforms": [
            (pygame.Rect(-10, SCREEN_HEIGHT - 40, 120, 40),  -75, -1,  0, 30, 0, -30), # tipo 1
            (pygame.Rect(500, SCREEN_HEIGHT - 40, 360, 120), hit_ground_x, -1,  0,  90, 0, -87), # tipo 2
            (pygame.Rect(950, SCREEN_HEIGHT - 40, 360, 120), hit_ground_x, -1,  0,  90, 0, -87),
            (pygame.Rect(1400, SCREEN_HEIGHT - 40, 360, 120), hit_ground_x, -1, 0,  90, 0, -87),
            (pygame.Rect(1850, SCREEN_HEIGHT - 40, 360, 120), hit_ground_x, -1, 0,  90, 0, -87),
        ],
        "gun_pos": (-260, 130),

        "other_platforms": [
            (pygame.Rect(-350, 150, 350, 20), 0, 0, 0, 0, 0, 0),
            (pygame.Rect(150, 450, 120, 40), hit_other_x, -1, 0, 30, 0, -30), # tipo 1
            (pygame.Rect(350, 350, 120, 40), hit_other_x, -1, 0, 30, 0, -30),
            (pygame.Rect(750, 370, 240, 80), -124, -1, 0, 60, 0, -60), # tipo 2
            (pygame.Rect(1000, 210, 240, 80), -124, -1, 0, 60, 0, -60),
            (pygame.Rect(1400, 250, 120, 40), hit_other_x, -1, 0, 30, 0, -30),
            (pygame.Rect(1750, 450, 120, 40), hit_other_x, -1, 0, 30, 0, -30),
        ],
        "rects_vermelhos": [
            (590, SCREEN_HEIGHT - 90, 100, 90,'espinho.png'), #200, 410 == 150, 450
            (350, 350, 40, 50,'espinho.jpeg'),
        ],
        "rects_azuis": [
            (0, SCREEN_HEIGHT - 90, 100, 90,"sprites/doublejump.png"),
           #1940, SCREEN_HEIGHT - 100
        ],


        "enemies_platform_indices": [1,2,3],
        "enemies_speeds": [1.5,1.6,1.7],
        "gate_start_pos": None,
        "gate_exit_pos": (2080, SCREEN_HEIGHT-120),
        "gate_exit_color": PURPLE,
    },

    {
        "ground_platforms": [
            (pygame.Rect(0, SCREEN_HEIGHT - 40, 2000, 140), -1, -1, 0, 0, 0, 0),
        ],
        
        "enemies_platform_indices": [],
        "enemies_speeds": [],
        "gate_start_pos": (10, SCREEN_HEIGHT - 120),
        "gate_start_color": ORANGE,
        "gate_exit_pos": None,
        "gate_exit_color": PURPLE,
    }
]


def load_phase(phase_index):
    phase_data = phases[phase_index]

    ground_data = phase_data.get("ground_platforms", [])
    other_data = phase_data.get("other_platforms", [])

    platforms = []
    ground_platforms = []
    other_platforms = []

    visual_platforms = []

    for item in ground_data:
        rect_base, inf_x, inf_y, extra_w, extra_h, img_off_x, img_off_y = item

        col_rect = rect_base.inflate(inf_x, inf_y)
        col_rect.midbottom = rect_base.midbottom

        platforms.append(col_rect)
        ground_platforms.append(item)
        visual_platforms.append(rect_base)

    for item in other_data:
        rect_base, inf_x, inf_y, extra_w, extra_h, img_off_x, img_off_y = item

        col_rect = rect_base.inflate(inf_x, inf_y)
        col_rect.midbottom = rect_base.midbottom

        platforms.append(col_rect)
        other_platforms.append(item)
        visual_platforms.append(rect_base)

    enemies = []

    if phase_index == 1:
        if ground_platforms:
            ultima_plataforma = ground_platforms[-1]
            boss_plataforma = ultima_plataforma[0] if isinstance(ultima_plataforma, tuple) else ultima_plataforma
            enemies.append(Boss(boss_plataforma, speed=2))
    else:
        for idx, spd in zip(
            phase_data.get("enemies_platform_indices", []),
            phase_data.get("enemies_speeds", [])
        ):
            if idx < len(platforms):
                enemies.append(Enemy(platforms[idx], speed=spd))


    rects_vermelhos = []
    for data in phase_data.get("rects_vermelhos", []):
        if len(data) == 5:
            x, y, w, h, img_name = data
            rects_vermelhos.append(RectVermelho(x, y, w, h, img_name))
        else:
            x, y, w, h = data
            rects_vermelhos.append(RectVermelho(x, y, w, h))
    rects_azuis = []
    for data in phase_data.get("rects_azuis", []):
        if len(data) == 5:
            x, y, w, h, img_name = data
            rects_azuis.append(RectAzul(x, y, w, h, img_name))
        else:
            x, y, w, h = data
            rects_azuis.append(RectAzul(x, y, w, h))

    boss = None
    if phase_index == 1:  # fase do boss
        boss = Boss(800, 300)

    gate_start = None
    gate_start_pos = phase_data.get("gate_start_pos", None)
    gate_start_color = phase_data.get("gate_start_color", ORANGE)
    gate_start_sprite = phase_data.get("gate_start_sprite", PORTAL_START_SPRITE)
    gate_start_sprite_offset = phase_data.get("gate_start_sprite_offset", PORTAL_START_SPRITE_OFFSET)
    gate_start_sprite_size = phase_data.get("gate_start_sprite_size", PORTAL_START_SPRITE_SIZE)

    if gate_start_pos is not None:
        gate_start = Gate(
            gate_start_pos[0], gate_start_pos[1],
            color=gate_start_color,
            sprite_path=gate_start_sprite,
            sprite_size=gate_start_sprite_size,
            sprite_offset=gate_start_sprite_offset,
        )
    gate_exit = None
    gate_exit_pos = phase_data.get("gate_exit_pos", None)
    gate_exit_color = phase_data.get("gate_exit_color", PURPLE)
    gate_exit_sprite = phase_data.get("gate_exit_sprite", PORTAL_EXIT_SPRITE)
    gate_exit_sprite_offset = phase_data.get("gate_exit_sprite_offset", PORTAL_EXIT_SPRITE_OFFSET)
    gate_exit_sprite_size = phase_data.get("gate_exit_sprite_size", PORTAL_EXIT_SPRITE_SIZE)
    if gate_exit_pos is not None:
        gate_exit = Gate(
            gate_exit_pos[0], gate_exit_pos[1],
            color=gate_exit_color,
            sprite_path=gate_exit_sprite,
            sprite_size=gate_exit_sprite_size,
            sprite_offset=gate_exit_sprite_offset,
        )
        
    return (
        platforms,
        ground_platforms,
        other_platforms,
        enemies,
        gate_start,
        gate_exit,
        rects_vermelhos,
        rects_azuis, 
        boss
    )

