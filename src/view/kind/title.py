from view import View, SharedViewData
from view.button import ViewButton

from typing import Optional
from pygame import Surface


class TitleView(View):

    # BACKGROUND_COLOR    = 54, 16, 12
    # BUTTON_NORMAL_COLOR = 133, 43, 24
    # BUTTON_OVER_COLOR   = 117, 37, 20

    def __init__(self):
        super().__init__()
        self._start_button: Optional[ViewButton] = None
        self._how_to_play: Optional[ViewButton] = None
        self._settings_button: Optional[ViewButton] = None
        self._credits_button: Optional[ViewButton] = None
        self._quit_button: Optional[ViewButton] = None
        self._title_surface: Optional[Surface] = None

    def _inner_init(self):

        self._start_button = ViewButton(45, "Play Now !")
        self._start_button.set_size(250, 80)
        self._start_button.set_action_callback(self._shared_data.get_show_view_callback("color_select"))
        self.add_child(self._start_button)

        self._how_to_play = ViewButton(31, "How To Play")
        self._how_to_play.set_size(250, 50)
        self._how_to_play.set_action_callback(self._shared_data.get_show_view_callback("how_to_play"))
        self.add_child(self._how_to_play)

        self._settings_button = ViewButton(25, "Settings")
        self._settings_button.set_size(200, 35)
        self._settings_button.set_action_callback(self._shared_data.get_show_view_callback("settings"))
        self.add_child(self._settings_button)

        self._credits_button = ViewButton(25, "Credits")
        self._credits_button.set_size(200, 35)
        self._credits_button.set_action_callback(self._shared_data.get_show_view_callback("credits"))
        self.add_child(self._credits_button)

        self._quit_button = ViewButton(25, "Quit")
        self._quit_button.set_size(200, 35)
        self._quit_button.set_action_callback(lambda e: self._shared_data.get_game().stop_game())
        self.add_child(self._quit_button)

        self._title_surface = self._shared_data.get_image("title.png")

    def _inner_pre_draw(self, surface: Surface):

        main_group_x = surface.get_width() / 2
        main_group_y = surface.get_height() / 2 + 100

        aux_group_x = surface.get_width() - 200 - 20
        aux_group_y = surface.get_height() - 20

        self._start_button.set_position_centered(main_group_x, main_group_y)
        self._how_to_play.set_position_centered(main_group_x, main_group_y + 80)
        self._settings_button.set_position(aux_group_x, aux_group_y - 115)
        self._credits_button.set_position(aux_group_x, aux_group_y - 75)
        self._quit_button.set_position(aux_group_x, aux_group_y - 35)

        title_pos = (
            main_group_x - (self._title_surface.get_width() / 2),
            120
        )

        surface.blit(self._title_surface, title_pos)
