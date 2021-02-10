from typing import Optional

from pygame import Surface

from view import View
from view.button import ViewButton


class EndView(View):

    def __init__(self):
        super().__init__()
        self._play_again_button: Optional[ViewButton] = None

    def _inner_init(self):
        self._play_again_button = ViewButton(45, "Play Again!", disabled = True)
        self._play_again_button.set_size(250,80)
        self._play_again_button.set_action_callback(self._shared_data.get_show_view_callback("color_select"))
        self.add_child(self._play_again_button)

    def _inner_pre_draw(self, surface: Surface):
        self._play_again_button.set_position_centered(surface.get_width()/2, 600)