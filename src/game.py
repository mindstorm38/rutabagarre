from typing import Optional
from pygame import Surface
import pygame


class Game:

    def __init__(self):
        self._screen: Optional[Surface] = None
        self._running: bool = False

    def start(self):

        # Init
        pygame.init()
        self._screen = pygame.display.set_mode((1024, 768))
        self._running = True

        # Loop
        while self._running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

            self._update()

        # Cleanup
        pass

    def _update(self):
        pass
