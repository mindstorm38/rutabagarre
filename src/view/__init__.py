from abc import ABC, abstractmethod
from typing import Optional, Dict

from pygame.font import Font
from pygame import Surface

import res


class CommonViewData:

    def __init__(self):
        self._fonts: Dict[int, Font] = {}

    def init(self):
        pass

    def cleanup(self):
        self._fonts = {}

    def get_font(self, size: int) -> Font:
        font = self._fonts.get(size)
        if font is None:
            font = Font(res.get_res("m5x7.ttf"), size)
            self._fonts[size] = font
        return font


class View(ABC):

    @abstractmethod
    def init(self, data: CommonViewData): ...

    @abstractmethod
    def draw(self, surface: Surface): ...


class Button:

    BUTTON_COLOR = (255, 255, 255)

    def __init__(self, font: Font, text: str):

        if font is None or text is None:
            raise ValueError("Font and text can't be None.")

        self._font = font
        self._text = text
        self._pos = (0, 0)

        self._surface: Optional[Surface] = None
        self._redraw()

    def _redraw(self):
        self._surface = self._font.render(self._text, True, self.BUTTON_COLOR)

    def set_position(self, x: float, y: float):
        self._pos = (x, y)

    def draw(self, surface: Surface):
        if self._surface is not None:
            surface.blit(self._surface, self._pos)
