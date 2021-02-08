from typing import Optional

from pygame import Surface

from . import View, CommonViewData, Button


class TitleView(View):

    def __init__(self):
        self._start_button: Optional[Button] = None

    def init(self, data: CommonViewData):
        self._start_button = Button(data.get_font(40), "Start")
        self._start_button.set_position(100, 100)

    def draw(self, surface: Surface):
        self._start_button.draw(surface)
