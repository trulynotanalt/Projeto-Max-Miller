# fases.py
import pygame
from inimigo import Enemy
from portao import Gate
from config import SCREEN_HEIGHT, PURPLE, ORANGE

phases = [
    {
        "ground_platforms": [
            pygame.Rect(0, SCREEN_HEIGHT - 40, 400, 40),
            pygame.Rect(500, SCREEN_HEIGHT - 40, 400, 40),
            pygame.Rect(950, SCREEN_HEIGHT - 40, 400, 40),
            pygame.Rect(1400, SCREEN_HEIGHT - 40, 400, 40),
            pygame.Rect(1850, SCREEN_HEIGHT - 40, 350, 40),
        ],
        "other_platforms": [
            pygame.Rect(150, 450, 120, 20),
            pygame.Rect(350, 350, 120, 20),
            pygame.Rect(550, 250, 120, 20),
            pygame.Rect(750, 400, 120, 20),
            pygame.Rect(900, 300, 120, 20),
            pygame.Rect(1150, 350, 120, 20),
            pygame.Rect(1400, 250, 120, 20),
            pygame.Rect(1650, 450, 120, 20),
            pygame.Rect(1900, 350, 100, 20),
        ],
        "enemies_platform_indices": [1, 3, 6, 7],
        "enemies_speeds": [2, 1.5, 2.5, 3],
        "gate_start_pos": None,
        "gate_exit_pos": (2300, SCREEN_HEIGHT - 40 - 80),
        "gate_exit_color": PURPLE,
    },

    {
        "ground_platforms": [
            pygame.Rect(0, SCREEN_HEIGHT - 40, 300, 40),
            pygame.Rect(400, SCREEN_HEIGHT - 40, 300, 40),
            pygame.Rect(850, SCREEN_HEIGHT - 40, 400, 40),
            pygame.Rect(1300, SCREEN_HEIGHT - 40, 400, 40),
            pygame.Rect(1750, SCREEN_HEIGHT - 40, 400, 40),
            pygame.Rect(2200, SCREEN_HEIGHT - 40, 350, 40),
        ],
        "other_platforms": [
            pygame.Rect(100, 450, 100, 20),
            pygame.Rect(300, 350, 140, 20),
            pygame.Rect(550, 250, 140, 20),
            pygame.Rect(800, 400, 100, 20),
            pygame.Rect(1050, 300, 140, 20),
            pygame.Rect(1300, 250, 120, 20),
            pygame.Rect(1600, 450, 150, 20),
            pygame.Rect(1900, 350, 140, 20),
            pygame.Rect(2150, 300, 100, 20),
        ],
        "enemies_platform_indices": [1, 3, 5, 7],
        "enemies_speeds": [2.5, 1.7, 3, 2],
        "gate_start_pos": (10, SCREEN_HEIGHT - 40 - 80),
        "gate_start_color": ORANGE,
        "gate_exit_pos": (2600, SCREEN_HEIGHT - 40 - 80),
        "gate_exit_color": PURPLE,
    }
]

def load_phase(phase_index):
    phase_data = phases[phase_index]
    ground_platforms = phase_data["ground_platforms"]
    other_platforms = phase_data["other_platforms"]
    platforms = ground_platforms + other_platforms

    enemies = []
    for idx, spd in zip(phase_data["enemies_platform_indices"], phase_data["enemies_speeds"]):
        if idx < len(platforms):
            enemy = Enemy(platforms[idx], speed=spd)
            enemies.append(enemy)

    gate_start_pos = phase_data.get("gate_start_pos", None)
    gate_start_color = phase_data.get("gate_start_color", PURPLE)
    gate_exit_pos = phase_data["gate_exit_pos"]
    gate_exit_color = phase_data.get("gate_exit_color", PURPLE)

    gate_start = None
    if gate_start_pos is not None:
        gate_start = Gate(gate_start_pos[0], gate_start_pos[1], color=gate_start_color)
    gate_exit = Gate(gate_exit_pos[0], gate_exit_pos[1], color=gate_exit_color)

    return platforms, ground_platforms, other_platforms, enemies, gate_start, gate_exit
