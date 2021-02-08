from typing import Optional
from pygame import Surface
import pygame


class Game:

    def __init__(self):
        self._screen: Optional[Surface] = None

    def start(self):

        pygame.init()

        self._screen = pygame.display.set_mode((1024, 768))
