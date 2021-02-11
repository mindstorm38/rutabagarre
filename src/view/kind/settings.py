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

        self._left_sound: Optional[ViewButton] = None
        self._right_sound: Optional[ViewButton] = None
        self._left_music: Optional[ViewButton] = None
        self._right_music: Optional[ViewButton] = None

        self._comingsoon_text: Optional[Surface] = None
        self._music_text: Optional[Surface] = None
        self._sound_text: Optional[Surface] = None
        self._music_percent_text: Optional[Surface] = None
        self._sound_percent_text: Optional[Surface] = None

        self._music_change = 0.3
        self._music_vol = 0

    def _inner_init(self):

        self._title = ViewButton(41, "Settings", disabled=True)
        self.add_child(self._title)

        self._return_button = ViewButton(35, "Return")
        self._return_button.set_size(150, 50)
        self._return_button.set_action_callback(self._shared_data.get_show_view_callback("title"))
        self.add_child(self._return_button)

        self._left_music = ViewButton(35, "<")
        self._left_music .set_size(50, 50)
        self._left_music .set_action_callback(self._change_music_vol(1))
        self.add_child(self._left_music )

        self._right_music = ViewButton(35, ">")
        self._right_music.set_size(50, 50)
        self._right_music.set_action_callback(self._change_music_vol(0))
        self.add_child(self._right_music)

        self._comingsoon_text = self._shared_data.get_font(50).render("Coming soon", True, self.TEXT_COLOR)

        self._music_text = self._shared_data.get_font(50).render("Music", True, self.TEXT_COLOR)
        self._sound_text = self._shared_data.get_font(50).render("Sound", True, self.TEXT_COLOR)

        self._music_percent_text = self._shared_data.get_font(50).render(str(int(self._music_vol*100)) + "%", True, self.TEXT_COLOR)

    def _change_music_vol(self, way: int):
        def _cb(_i) :
            if way == 1 :
                if pygame.mixer.music.get_volume() < 0.1:
                    pygame.mixer.music.set_volume(0.0)
                else :
                    pygame.mixer.music.set_volume(pygame.mixer.music.get_volume()  - 0.1)
            else :
                pygame.mixer.music.set_volume(pygame.mixer.music.get_volume()  + 0.1)
            self._shared_data.get_game().show_view("settings")
        return _cb

    def _inner_pre_draw(self, surface: Surface):
        surface_width, surface_height = surface.get_size()
        x_mid = surface_width / 2

        pygame.draw.rect(surface, self.BUTTON_NORMAL_COLOR, (100, 120, surface_width - 200, surface_height - 240))
        pygame.draw.rect(surface, self.BACKGROUND_COLOR, (200, 250, 200, 200))

        pygame.draw.line(surface, self.TEXT_COLOR, (200, 250), (800, 250), 2)
        pygame.draw.line(surface, self.TEXT_COLOR, (200, 350), (800, 350), 2)
        pygame.draw.line(surface, self.TEXT_COLOR, (200, 450), (800, 450), 2)

        pygame.draw.line(surface, self.TEXT_COLOR, (200, 250), (200, 450), 2)
        pygame.draw.line(surface, self.TEXT_COLOR, (400, 250), (400, 450), 2)
        pygame.draw.line(surface, self.TEXT_COLOR, (800, 250), (800, 450), 2)

        self._title.set_position_centered(x_mid, 60)
        self._return_button.set_position(20, surface_height - 20 - 50)

        self._right_music.set_position_centered(750, 300)
        self._left_music.set_position_centered(450, 300)

        surface.blit(self._comingsoon_text, (500, 385))
        surface.blit(self._music_text, (255, 290))
        surface.blit(self._sound_text, (250, 385))
        surface.blit(self._music_percent_text, (570, 290))

    def on_enter(self):
        self._music_percent_text = self._shared_data.get_font(50).render(str(int(pygame.mixer.music.get_volume()*100)) + "%", True, self.TEXT_COLOR)