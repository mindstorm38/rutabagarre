from typing import Optional

from view.button import ViewButton
from view import View

from pygame import Surface
import pygame


class ViewLightButton(ViewButton):

    def _get_color(self):
        return self._view.BACKGROUND_COLOR

class SettingsView(View):

    def __init__(self):

        super().__init__()

        self._return_button: Optional[ViewButton] = None
        self._title: Optional[ViewButton] = None

        self._comingsoon_text: Optional[Surface] = None

    def _inner_init(self):

        self._title = ViewButton(41, "Settings", disabled=True)
        self.add_child(self._title)

        self._return_button = ViewButton(35, "Return")
        self._return_button.set_size(150, 50)
        self._return_button.set_action_callback(self._shared_data.get_show_view_callback("title"))
        self.add_child(self._return_button)

        self._comingsoon_text = self._shared_data.get_font(50).render("Coming soon", True, self.TEXT_COLOR)

    def _inner_pre_draw(self, surface: Surface):
        surface_width, surface_height = surface.get_size()
        x_mid = surface_width / 2

        pygame.draw.rect(surface, self.BUTTON_NORMAL_COLOR, (100, 120, surface_width - 200, surface_height - 240))

        self._title.set_position_centered(x_mid, 60)
        self._return_button.set_position(20, surface_height - 20 - 50)

        surface.blit(self._comingsoon_text, (x_mid-90, 370))