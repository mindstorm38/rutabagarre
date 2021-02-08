from typing import Optional
from pygame import Surface
import pygame

from stage import Stage


__all__ = ["Game"]


class Game:

    def __init__(self):
        self._surface: Optional[Surface] = None
        self._running: bool = False
        self._stage: Optional[Stage] = None

    def start(self):

        # Init
        pygame.init()
        self._surface = pygame.display.set_mode((1024, 768))
        self._running = True

        # Loop
        while self._running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

            self._update()

            pygame.display.flip()

        # Cleanup
        pygame.quit()

    def _update(self):
        if self._stage is not None:
            self._stage.update()
