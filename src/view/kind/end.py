from typing import Optional
from view import View
from view.button import ViewButton
from pygame import Surface
import pygame


class EndView(View):

    def __init__(self):
        super().__init__()
        self._winner_button: Optional[ViewButton] = None
        self._play_again_button: Optional[ViewButton] = None
        self._change_settings_button: Optional[ViewButton] = None
        self._quit_button: Optional[ViewButton] = None
        self._credits_button: Optional[ViewButton] = None

        self._player_one_surface: Optional[Surface] = None

    def _inner_init(self):
        self._winner_button = ViewButton(45, "P2 wins!", disabled=True)
        self._winner_button.set_size(300, 100)
        self.add_child(self._winner_button)

        self._play_again_button = ViewButton(45, "Play Again!")
        self._play_again_button.set_size(250, 80)
        self._play_again_button.set_action_callback(self._shared_data.get_show_view_callback("color_select"))
        self.add_child(self._play_again_button)

        self._change_settings_button = ViewButton(30, "Change settings")
        self._change_settings_button.set_size(180, 50)
        self._change_settings_button.set_action_callback(self._shared_data.get_show_view_callback("color_select"))
        self.add_child(self._change_settings_button)

        self._quit_button = ViewButton(20, "Quit")
        self._quit_button.set_size(100, 30)
        self._quit_button.set_action_callback(self._shared_data.get_show_view_callback("title"))
        self.add_child(self._quit_button)

        self._credits_button = ViewButton(20, "Credits")
        self._credits_button.set_size(100, 30)
        self._credits_button.set_action_callback(self._shared_data.get_show_view_callback("credits"))
        self.add_child(self._credits_button)

        self._player_one_surface = self._shared_data.get_image("credits/tete.png")

    def _inner_pre_draw(self, surface: Surface):

        main_group_x = surface.get_width()/2
        surface_width, surface_height = surface.get_size()

        pygame.draw.rect(surface, self.BUTTON_NORMAL_COLOR, (250, 200, 230, 300))
        pygame.draw.rect(surface, self.BUTTON_NORMAL_COLOR, (550, 200, 230, 300))

        self._winner_button.set_position_centered(main_group_x, 100)
        self._play_again_button.set_position_centered(main_group_x, 600)
        self._change_settings_button.set_position_centered(main_group_x, 680)
        self._quit_button.set_position_centered(80, 730)
        self._credits_button.set_position_centered(940, 730)

        player_one_pos = (
            90, 300
        )

        surface.blit(self._player_one_surface, player_one_pos)
