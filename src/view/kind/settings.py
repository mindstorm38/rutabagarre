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

        self._music_change = 0.0
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
        self._left_music .set_action_callback(self._change_vol(-1, "music"))
        self.add_child(self._left_music)

        self._right_music = ViewButton(35, ">")
        self._right_music.set_size(50, 50)
        self._right_music.set_action_callback(self._change_vol(1, "music"))
        self.add_child(self._right_music)

        self._left_sound = ViewButton(35, "<")
        self._left_sound .set_size(50, 50)
        self._left_sound .set_action_callback(self._change_vol(-1, "sound"))
        self.add_child(self._left_sound)

        self._right_sound = ViewButton(35, ">")
        self._right_sound.set_size(50, 50)
        self._right_sound.set_action_callback(self._change_vol(1, "sound"))
        self.add_child(self._right_sound)

        self._music_text = self._shared_data.get_font(50).render("Music", True, self.TEXT_COLOR)
        self._sound_text = self._shared_data.get_font(50).render("Sound", True, self.TEXT_COLOR)

    def _change_vol(self, way: int, typ: str):
        def _cb(_i):
            if typ == "music":
                self._shared_data.music_volume = max(0.0, min(1.0, self._shared_data.music_volume + way * 0.01))
            elif typ == "sound":
                self._shared_data.sound_volume = max(0.0, min(1.0, self._shared_data.sound_volume + way * 0.01))
            self._redraw()
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
        self._right_sound.set_position_centered(750, 410)
        self._left_sound.set_position_centered(450, 410)

        surface.blit(self._music_text, (255, 290))
        surface.blit(self._sound_text, (250, 385))

        if self._music_percent_text is not None:
            surface.blit(self._music_percent_text, (570, 290))

        if self._sound_percent_text is not None:
            surface.blit(self._sound_percent_text, (570, 385))

    def _redraw(self):
        self._music_percent_text = self._shared_data.get_font(50).render("{:.2f}%".format(self._shared_data.music_volume * 100.0), True, self.TEXT_COLOR)
        self._sound_percent_text = self._shared_data.get_font(50).render("{:.2f}%".format(self._shared_data.sound_volume * 100.0), True, self.TEXT_COLOR)

    def on_enter(self):
        self._redraw()
