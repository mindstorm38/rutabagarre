from typing import Optional

from pygame import Surface

from . import View, SharedViewData, Button


class TitleView(View):

    BACKGROUND_COLOR = (54, 16, 12)

    def __init__(self):
        self._start_button: Optional[Button] = None
        self._settings_button: Optional[Button] = None

    def init(self, data: SharedViewData):

        self._start_button = Button(data.get_font(45), "Play Now !")
        self._start_button.set_size(200, 80)

        self._settings_button = Button(data.get_font(35), "Settings")
        self._settings_button.set_size(200, 45)

    def draw(self, surface: Surface):

        surface.fill(self.BACKGROUND_COLOR)

        x_mid = surface.get_width() / 2
        y_mid = surface.get_height() / 2

        self._start_button.set_position_centered(x_mid, y_mid)
        self._start_button.draw(surface)

        self._settings_button.set_position_centered(x_mid, y_mid + 100)
        self._settings_button.draw(surface)
