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
    }
]


KEYS_PLAYERS = {}


for i, controls in enumerate(PLAYERS_KEYS):
    for control, key in controls.items():
        KEYS_PLAYERS[key] = (i, control)
