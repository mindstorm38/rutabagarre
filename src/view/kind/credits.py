from typing import Optional

from view.button import ViewButton
from view import View

from pygame import Surface
import pygame


class ViewLightButton(ViewButton):

    def _get_color(self):
        return self._view.BACKGROUND_COLOR


class CreditsView(View):

    def __init__(self):

        super().__init__()

        self._title: Optional[ViewButton] = None
        self._code_title: Optional[ViewLightButton] = None
        self._graphics_title: Optional[ViewLightButton] = None
        self._music_title: Optional[ViewLightButton] = None
        self._sound_title: Optional[ViewLightButton] = None

        self._music_text: Optional[Surface] = None
        self._sound_text: Optional[Surface] = None

        self._return_button: Optional[ViewButton] = None

        self._authors = []

        self._add_credit("credits/nath.png", "Nathan Rousseau")
        self._add_credit("credits/tete.png", "Theo Rozier")
        self._add_credit("credits/pl.png", "Pierre-Loup C.P.")
        self._add_credit("credits/cece.png", "Celia Martin", x_off=-20)

    def _add_credit(self, res_path: str, name: str, *, x_off: int = 0):
        self._authors.append({
            "res": res_path,
            "name": name,
            "surface": None,
            "x_off": x_off,
            "title": None
        })

    def _inner_init(self):

        self._title = ViewButton(41, "Credits", disabled=True)
        self.add_child(self._title)

        self._code_title = ViewLightButton(35, "Code", disabled=True)
        self._code_title.set_size(150, 40)
        self.add_child(self._code_title)

        self._graphics_title = ViewLightButton(35, "Graphics", disabled=True)
        self._graphics_title.set_size(150, 40)
        self.add_child(self._graphics_title)

        self._music_title = ViewLightButton(31, "Music", disabled=True)
        self._music_title.set_size(120, 35)
        self.add_child(self._music_title)

        self._sound_title = ViewLightButton(31, "Sound", disabled=True)
        self._sound_title.set_size(120, 35)
        self.add_child(self._sound_title)

        self._music_text = self._shared_data.get_font(25).render("Gautier Bois - PRMNNT", True, self.TEXT_COLOR)
        self._sound_text = self._shared_data.get_font(25).render("https://mixkit.co", True, self.TEXT_COLOR)

        self._return_button = ViewButton(35, "Return")
        self._return_button.set_size(150, 50)
        self._return_button.set_action_callback(self._shared_data.get_show_view_callback("title"))
        self.add_child(self._return_button)

        for author in self._authors:
            author["surface"] = self._shared_data.get_image(author["res"])
            author["x_off"] -= author["surface"].get_width() / 2
            author["title"] = title = ViewLightButton(25, author["name"], disabled=True)
            title.set_size(160, 30)
            self.add_child(title)

    def _inner_pre_draw(self, surface: Surface):

        surface_width, surface_height = surface.get_size()
        x_mid = surface_width / 2

        pygame.draw.rect(surface, self.BUTTON_NORMAL_COLOR, (100, 120, surface_width - 200, surface_height - 240))

        self._title.set_position_centered(x_mid, 60)
        self._code_title.set_position_centered(x_mid - 200, 170)
        self._graphics_title.set_position_centered(x_mid + 200, 170)

        self._music_title.set_position_centered(x_mid - 200, 580)
        self._sound_title.set_position_centered(x_mid + 200, 580)
        surface.blit(self._music_text, (x_mid - 200 - self._music_text.get_width() / 2, 610))
        surface.blit(self._sound_text, (x_mid + 200 - self._sound_text.get_width() / 2, 610))

        self._return_button.set_position(20, surface_height - 20 - 50)

        arts_y = 480
        arts_x = x_mid - 300

        for author in self._authors:
            surface.blit(author["surface"], (arts_x + author["x_off"], arts_y - author["surface"].get_height()))
            author["title"].set_position_centered(arts_x, arts_y + 30)
            arts_x += 200
