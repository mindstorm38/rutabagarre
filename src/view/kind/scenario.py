from typing import Optional
from view import View
from view.button import ViewButton
from pygame import Surface
import pygame

class ScenarioView(View):

    def __init__(self):

        super().__init__()

        self._start_button: Optional[ViewButton] = None
        self._winner_button: Optional[ViewButton] = None

    def _inner_init(self):

        self._start_button = ViewButton(45, "Start")
        self._start_button.set_size(200, 70)
        self._start_button.set_action_callback(self._shared_data.get_show_view_callback("title"))
        self.add_child(self._start_button)

        self._scenario_button = ViewButton(45, "Scenario", disabled=True)
        self._scenario_button.set_size(300, 100)
        self.add_child(self._scenario_button)

        self._line_one_text = self._shared_data.get_font(40).render("A few farmers were sharing the same field.", True, self.TEXT_COLOR)
        self._line_two_text = self._shared_data.get_font(40).render("But one day...", True, self.TEXT_COLOR)
        self._line_three_text = self._shared_data.get_font(40).render("One of them didn't pay his rent.", True, self.TEXT_COLOR)
        self._line_four_text = self._shared_data.get_font(40).render("Because they are warn-blooded", True, self.TEXT_COLOR)
        self._line_five_text = self._shared_data.get_font(40).render("a fight begins.", True, self.TEXT_COLOR)
        self._line_six_text = self._shared_data.get_font(40).render("With the help of their plants,", True, self.TEXT_COLOR)
        self._line_seven_text = self._shared_data.get_font(40).render("they can gain special power to win the battle.", True, self.TEXT_COLOR)

    def _inner_pre_draw(self, surface: Surface):

        height = surface.get_height()
        width = surface.get_width()

        self._start_button.set_position_centered(width - 150, height - 80)
        self._scenario_button.set_position_centered(width/2, 75)

        pygame.draw.rect(surface, self.BUTTON_NORMAL_COLOR, (100, 200, 824, 400))
        surface.blit(self._line_one_text, (260, 240))
        surface.blit(self._line_two_text, (425, 280+10))
        surface.blit(self._line_three_text, (330, 320+20))
        surface.blit(self._line_four_text, (323, 360+30))
        surface.blit(self._line_five_text, (425, 400+40))
        surface.blit(self._line_six_text, (340, 440+50))
        surface.blit(self._line_seven_text, (250, 480+60))