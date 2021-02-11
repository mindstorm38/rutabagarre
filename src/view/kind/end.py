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

        #self._player_one_surface: Optional[Surface] = None

    def _inner_init(self):
        self._winner_button = ViewButton(45, "P2 wins!", disabled=True)
        self._winner_button.set_size(300, 100)
        self.add_child(self._winner_button)

        self._play_again_button = ViewButton(45, "Play Again!")
        self._play_again_button.set_size(200, 70)
        self._play_again_button.set_action_callback(self._shared_data.get_show_view_callback("color_select"))
        self.add_child(self._play_again_button)

        self._change_settings_button = ViewButton(20, "Change settings")
        self._change_settings_button.set_size(150, 30)
        self._change_settings_button.set_action_callback(self._shared_data.get_show_view_callback("color_select"))
        self.add_child(self._change_settings_button)

        self._quit_button = ViewButton(20, "Quit")
        self._quit_button.set_size(100, 30)
        self._quit_button.set_action_callback(self._shared_data.get_show_view_callback("title"))
        self.add_child(self._quit_button)

        #self._player_one_surface = self._shared_data.get_image("credits/tete.png")

        self._ko_one_text = self._shared_data.get_font(32).render("KOs", True, self.TEXT_COLOR)
        self._plants_collected_one_text = self._shared_data.get_font(32).render("Plants collected", True, self.TEXT_COLOR)
        self._damage_dealt_one_text = self._shared_data.get_font(32).render("Damage dealt", True, self.TEXT_COLOR)
        self._damage_taken_one_text = self._shared_data.get_font(32).render("Damage taken", True, self.TEXT_COLOR)

        self._ko_two_text = self._shared_data.get_font(32).render("KOs", True, self.TEXT_COLOR)
        self._plants_collected_two_text = self._shared_data.get_font(32).render("Plants collected", True, self.TEXT_COLOR)
        self._damage_dealt_two_text = self._shared_data.get_font(32).render("Damage dealt", True, self.TEXT_COLOR)
        self._damage_taken_two_text = self._shared_data.get_font(32).render("Damage taken", True, self.TEXT_COLOR)

    def _inner_pre_draw(self, surface: Surface):

        main_group_x = surface.get_width()/2
        surface_width, surface_height = surface.get_size()

        self._winner_button.set_position_centered(main_group_x, 75)
        self._play_again_button.set_position_centered(main_group_x, 700)
        self._change_settings_button.set_position_centered(925, 730)
        self._quit_button.set_position_centered(80, 730)

        #player_one_pos = (
        #    90, 300
        #)

        #surface.blit(self._player_one_surface, player_one_pos)

        #tableau 1
        pygame.draw.rect(surface, self.BUTTON_NORMAL_COLOR, (20, 150, 229, 252))

        pygame.draw.line(surface, self.TEXT_COLOR, (20, 150), (248, 150), 1)
        pygame.draw.line(surface, self.TEXT_COLOR, (20, 213), (248, 213), 1)
        pygame.draw.line(surface, self.TEXT_COLOR, (20, 276), (248, 276), 1)
        pygame.draw.line(surface, self.TEXT_COLOR, (20, 339), (248, 339), 1)
        pygame.draw.line(surface, self.TEXT_COLOR, (20, 402), (248, 402), 1)

        surface.blit(self._ko_one_text, (27, 171))
        surface.blit(self._plants_collected_one_text, (27, 234))
        surface.blit(self._damage_dealt_one_text, (27, 297))
        surface.blit(self._damage_taken_one_text, (27, 360))

        #tableau 2
        pygame.draw.rect(surface, self.BUTTON_NORMAL_COLOR, (270, 150, 229, 252))

        pygame.draw.line(surface, self.TEXT_COLOR, (270, 150), (498, 150), 1)
        pygame.draw.line(surface, self.TEXT_COLOR, (270, 213), (498, 213), 1)
        pygame.draw.line(surface, self.TEXT_COLOR, (270, 276), (498, 276), 1)
        pygame.draw.line(surface, self.TEXT_COLOR, (270, 339), (498, 339), 1)
        pygame.draw.line(surface, self.TEXT_COLOR, (270, 402), (498, 402), 1)

        surface.blit(self._ko_two_text, (277, 171))
        surface.blit(self._plants_collected_two_text, (277, 234))
        surface.blit(self._damage_dealt_two_text, (277, 297))
        surface.blit(self._damage_taken_two_text, (277, 360))

        # tableau 3
        pygame.draw.rect(surface, self.BUTTON_NORMAL_COLOR, (520, 150, 229, 252))

        pygame.draw.line(surface, self.TEXT_COLOR, (520, 150), (748, 150), 1)
        pygame.draw.line(surface, self.TEXT_COLOR, (520, 213), (748, 213), 1)
        pygame.draw.line(surface, self.TEXT_COLOR, (520, 276), (748, 276), 1)
        pygame.draw.line(surface, self.TEXT_COLOR, (520, 339), (748, 339), 1)
        pygame.draw.line(surface, self.TEXT_COLOR, (520, 402), (748, 402), 1)

        surface.blit(self._ko_two_text, (527, 171))
        surface.blit(self._plants_collected_two_text, (527, 234))
        surface.blit(self._damage_dealt_two_text, (527, 297))
        surface.blit(self._damage_taken_two_text, (527, 360))

        # tableau 4
        pygame.draw.rect(surface, self.BUTTON_NORMAL_COLOR, (770, 150, 229, 252))

        pygame.draw.line(surface, self.TEXT_COLOR, (770, 150), (998, 150), 1)
        pygame.draw.line(surface, self.TEXT_COLOR, (770, 213), (998, 213), 1)
        pygame.draw.line(surface, self.TEXT_COLOR, (770, 276), (998, 276), 1)
        pygame.draw.line(surface, self.TEXT_COLOR, (770, 339), (998, 339), 1)
        pygame.draw.line(surface, self.TEXT_COLOR, (770, 402), (998, 402), 1)

        surface.blit(self._ko_two_text, (777, 171))
        surface.blit(self._plants_collected_two_text, (777, 234))
        surface.blit(self._damage_dealt_two_text, (777, 297))
        surface.blit(self._damage_taken_two_text, (777, 360))
