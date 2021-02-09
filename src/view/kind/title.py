from view import View, SharedViewData
from view.button import ViewButton

from typing import Optional
from pygame import Surface


class TitleView(View):

    BACKGROUND_COLOR    = 54, 16, 12
    BUTTON_NORMAL_COLOR = 133, 43, 24
    BUTTON_OVER_COLOR   = 117, 37, 20

    def __init__(self):
        super().__init__()
        self._start_button: Optional[ViewButton] = None
        self._settings_button: Optional[ViewButton] = None

    def _inner_init(self):

        self._start_button = ViewButton(45, "Play Now !")
        self._start_button.set_size(250, 80)
        self._start_button.set_action_callback(self._shared_data.get_show_view_callback("color_select"))
        self.add_child(self._start_button)

        self._settings_button = ViewButton(35, "Settings")
        self._settings_button.set_size(250, 45)
        self.add_child(self._settings_button)

    def _inner_pre_draw(self, surface: Surface):

        x_mid = surface.get_width() / 2
        y_mid = surface.get_height() / 2

        self._start_button.set_position_centered(x_mid, y_mid)
        self._settings_button.set_position_centered(x_mid, y_mid + 100)
