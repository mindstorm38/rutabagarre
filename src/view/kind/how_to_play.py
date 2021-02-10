from typing import Optional

from view.button import ViewButton
from view import View

from pygame import Surface
import pygame


class ViewLightButton(ViewButton):

    def _get_color(self):
        return self._view.BACKGROUND_COLOR


class HowToPlayView(View):

    def __init__(self):

        super().__init__()

        self._return_button : Optional[ViewButton] = None

    def _inner_init(self):
        self._return_button = ViewButton(35, "Return")
        self._return_button.set_size(150, 50)
        self._return_button.set_action_callback(self._shared_data.get_show_view_callback("title"))
        self.add_child(self._return_button)


    def _inner_pre_draw(self, surface: Surface):
        pass

