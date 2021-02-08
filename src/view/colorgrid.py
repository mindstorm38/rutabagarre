from typing import Optional

from pygame.event import Event
from pygame import Surface
import pygame

from . import ViewObject


class ColorGrid(ViewObject):

    def __init__(self):
        super().__init__(700, 200)
        self._grid_surface: Optional[Surface] = None

    def _redraw(self):
        self._grid_surface = Surface(self._size)

    # Méthodes override #

    def draw(self, surface: Surface):
        pass

    def event(self, event: Event):
        pass
