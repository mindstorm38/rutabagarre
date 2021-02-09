import pygame


PLAYERS_KEYS = [
    {
        "up": pygame.K_z,
        "down": pygame.K_s,
        "left": pygame.K_q,
        "right": pygame.K_d
    },
    {
        "up": pygame.K_i,
        "down": pygame.K_k,
        "left": pygame.K_j,
        "right": pygame.K_l
    },
    {
        "up": pygame.K_UP,
        "down": pygame.K_DOWN,
        "left": pygame.K_LEFT,
        "right": pygame.K_RIGHT
    },
    {
        "up": pygame.K_KP8,
        "down": pygame.K_KP5,
        "left": pygame.K_KP4,
        "right": pygame.K_KP6
    }
]


KEYS_PLAYERS = {}


for i, controls in enumerate(PLAYERS_KEYS):
    for control, key in controls.items():
        KEYS_PLAYERS[key] = (i, control)
