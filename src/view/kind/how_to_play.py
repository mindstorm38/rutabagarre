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

        self._num = 0

        self._return_button : Optional[ViewButton] = None
        self._title: Optional[ViewButton] = None

        self._left: Optional[ViewButton] = None
        self._right: Optional[ViewButton] = None

        self._character_type_text: Optional[Surface] = None
        self._character_name_text: Optional[Surface] = None
        self._joke_text: Optional[Surface] = None

        self._walk_text: Optional[Surface] = None
        self._run_text: Optional[Surface] = None
        self._jump_text: Optional[Surface] = None
        self._collect_text: Optional[Surface] = None
        self._superhit_text: Optional[Surface] = None
        self._hit_text: Optional[Surface] = None

        self._symb_RL_text: Optional[Surface] = None
        self._symb_runRL_text: Optional[Surface] = None
        self._symb_up_text: Optional[Surface] = None
        self._symb_down_text: Optional[Surface] = None
        self._symb_superhit_text: Optional[Surface] = None
        self._symb_hit_text: Optional[Surface] = None

        self._letter_RL_text: Optional[Surface] = None
        self._letter_runRL_text: Optional[Surface] = None
        self._letter_up_text: Optional[Surface] = None
        self._letter_down_text: Optional[Surface] = None
        self._letter_superhit_text: Optional[Surface] = None
        self._letter_hit_text: Optional[Surface] = None

        self._authors = []
        self._image : Optional[Surface] = None

        self._add_charact("howtoplay/farmer.png", "Farmer", "Base character", "NONE", "Yes yes yes")
        self._add_charact("howtoplay/potato.png", "Potato", "Hand-to-Hand attack", "X", "Yes yes yes")
        self._add_charact("howtoplay/corn.png", "Corn", "Ranged attack", "X", "COMING SOON")
        self._add_charact("howtoplay/mushroom.png", "Mushroom", "Smock attack", "X", "COMING SOON")
        self._add_charact("howtoplay/carrot.png", "Carrot", "Sword attack", "X", "COMING SOON")
        self._add_charact("howtoplay/chilli.png", "Chilli", "Fire attack", "X", "COMING SOON")

    def _add_charact(self, res_path: str, name: str, type: str, specialhit: str, joke: str):
        self._authors.append({
            "res": res_path,
            "name": name,
            "typechar":type,
            "commandesuperhit":specialhit,
            "joke":joke
        })

    def _inner_init(self):
        self._title = ViewButton(41, "How to play", disabled=True)
        self.add_child(self._title)

        self._return_button = ViewButton(35, "Return")
        self._return_button.set_size(150, 50)
        self._return_button.set_action_callback(self._shared_data.get_show_view_callback("title"))
        self.add_child(self._return_button)

        self._left = ViewButton(35, ">")
        self._left.set_size(50, 50)
        self._left.set_action_callback(self._next_element_character_list(1))
        self.add_child(self._left)

        self._right = ViewButton(35, "<")
        self._right.set_size(50, 50)
        self._right.set_action_callback(self._next_element_character_list(0))
        self.add_child(self._right)

        self._character_name_text = self._shared_data.get_font(50).render(self._authors[self._num]["name"], True, self.TEXT_COLOR)
        self._character_type_text = self._shared_data.get_font(50).render(self._authors[self._num]["typechar"], True, self.TEXT_COLOR)
        self._joke_text = self._shared_data.get_font(25).render(self._authors[self._num]["joke"], True, self.TEXT_COLOR)

        self._walk_text = self._shared_data.get_font(40).render("Walk", True, self.TEXT_COLOR)
        self._run_text = self._shared_data.get_font(40).render("Run", True, self.TEXT_COLOR)
        self._jump_text = self._shared_data.get_font(40).render("Jump", True, self.TEXT_COLOR)
        self._collect_text = self._shared_data.get_font(40).render("Collect/Sleep", True, self.TEXT_COLOR)
        self._superhit_text = self._shared_data.get_font(40).render("Super hit", True, self.TEXT_COLOR)
        self._hit_text = self._shared_data.get_font(40).render("Hit", True, self.TEXT_COLOR)

        self._RL_text = self._shared_data.get_font(40).render("<- -> / Q D", True, self.TEXT_COLOR)
        self._runRL_text = self._shared_data.get_font(40).render("<- -> / Q D", True, self.TEXT_COLOR)
        self._up_text = self._shared_data.get_font(40).render("up / Z", True, self.TEXT_COLOR)
        self._down_text = self._shared_data.get_font(40).render("down / S", True, self.TEXT_COLOR)
        self._input_superhit_text = self._shared_data.get_font(40).render(self._authors[self._num]["commandesuperhit"], True, self.TEXT_COLOR)
        self._input_hit_text = self._shared_data.get_font(40).render("? / C", True, self.TEXT_COLOR)

        self._image = self._shared_data.get_image(self._authors[self._num]["res"])

    def on_enter(self):
        self._character_name_text = self._shared_data.get_font(50).render(self._authors[self._num]["name"], True, self.TEXT_COLOR)
        self._character_type_text = self._shared_data.get_font(50).render(self._authors[self._num]["typechar"], True, self.TEXT_COLOR)
        self._joke_text = self._shared_data.get_font(25).render(self._authors[self._num]["joke"], True, self.TEXT_COLOR)
        self._input_superhit_text = self._shared_data.get_font(40).render(self._authors[self._num]["commandesuperhit"], True, self.TEXT_COLOR)
        self._image = self._shared_data.get_image(self._authors[self._num]["res"])

    def _next_element_character_list(self, way: int):
        def _cb(_i) :
            if way is 1 :
                self._num = self._num + 1
                if self._num > 5 :
                    self._num = 0
            else :
                self._num = self._num - 1
                if self._num < 0 :
                    self._num = 5
            self._shared_data.get_game().show_view("how_to_play")
        return _cb

    def _inner_pre_draw(self, surface: Surface):
        surface_width, surface_height = surface.get_size()
        x_mid = surface_width / 2

        pygame.draw.rect(surface, self.BUTTON_NORMAL_COLOR, (100, 120, surface_width - 200, surface_height - 240))
        pygame.draw.rect(surface, self.BACKGROUND_COLOR, (500, 150, 200, 350))

        pygame.draw.line(surface, self.TEXT_COLOR, (500,150) , (900,150) ,2)
        pygame.draw.line(surface, self.TEXT_COLOR, (500, 200), (900, 200), 2)
        pygame.draw.line(surface, self.TEXT_COLOR, (500, 260), (900, 260), 2)
        pygame.draw.line(surface, self.TEXT_COLOR, (500, 320), (900, 320), 2)
        pygame.draw.line(surface, self.TEXT_COLOR, (500, 380), (900, 380), 2)
        pygame.draw.line(surface, self.TEXT_COLOR, (500, 440), (900, 440), 2)
        pygame.draw.line(surface, self.TEXT_COLOR, (500, 500), (900, 500), 2)

        pygame.draw.line(surface, self.TEXT_COLOR, (500, 150), (500, 500), 2)
        pygame.draw.line(surface, self.TEXT_COLOR, (700, 150), (700, 500), 2)
        pygame.draw.line(surface, self.TEXT_COLOR, (900, 150), (900, 500), 2)


        self._title.set_position_centered(x_mid, 60)
        self._return_button.set_position(20, surface_height - 20 - 50)

        self._right.set_position_centered(150, 400)
        self._left.set_position_centered(450, 400)

        surface.blit(self._character_name_text, (x_mid - 200 - self._character_name_text.get_width() / 2, 150))
        surface.blit(self._character_type_text, (x_mid - 200 - self._character_type_text.get_width() / 2, 580))
        surface.blit(self._joke_text, (x_mid + 200 - self._joke_text.get_width() / 2, 550))

        surface.blit(self._walk_text, (575, 160))
        surface.blit(self._run_text, (575, 220))
        surface.blit(self._jump_text, (570, 280))
        surface.blit(self._collect_text, (520, 340))
        surface.blit(self._hit_text, (580, 400))
        surface.blit(self._superhit_text, (540, 460))

        surface.blit(self._RL_text, (730,160))
        surface.blit(self._runRL_text, (730,220))
        surface.blit(self._up_text, (750,280))
        surface.blit(self._down_text, (750,340))
        surface.blit(self._input_hit_text, (760,400))
        surface.blit(self._input_superhit_text, (760,460))

        surface.blit(self._image, (155,235))