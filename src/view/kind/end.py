from view.anim import FARMER_ANIMATION, AnimTracker
from view import View, AnimSurfaceColored
from view.button import ViewButton
from typing import Optional
from pygame import Surface
import pygame
from view.player import get_player_color
from stage import Stage


class EndView(View):

    def __init__(self):
        super().__init__()
        self._winner_button: Optional[ViewButton] = None
        self._play_again_button: Optional[ViewButton] = None
        self._quit_button: Optional[ViewButton] = None
        self._credits_button: Optional[ViewButton] = None

        self._player_anim_surface: Optional[AnimSurfaceColored] = None
        self._player_anim_tracker = AnimTracker()
        self._player_anim_tracker.push_infinite_anim("idle", 4)

        self._ko_text: Optional[Surface] = None
        self._plants_collected_text: Optional[Surface] = None
        self._damage_dealt_text: Optional[Surface] = None
        self._damage_taken_text: Optional[Surface] = None

        self._ko_p1_text: Optional[Surface] = None
        self._plants_collected_p1_text: Optional[Surface] = None
        self._damage_dealt_p1_text: Optional[Surface] = None
        self._damage_taken_p1_text: Optional[Surface] = None

        self._ko_p2_text: Optional[Surface] = None
        self._plants_collected_p2_text: Optional[Surface] = None
        self._damage_dealt_p2_text: Optional[Surface] = None
        self._damage_taken_p2_text: Optional[Surface] = None

        self._ko_p3_text: Optional[Surface] = None
        self._plants_collected_p3_text: Optional[Surface] = None
        self._damage_dealt_p3_text: Optional[Surface] = None
        self._damage_taken_p3_text: Optional[Surface] = None

        self._ko_p4_text: Optional[Surface] = None
        self._plants_collected_p4_text: Optional[Surface] = None
        self._damage_dealt_p4_text: Optional[Surface] = None
        self._damage_taken_p4_text: Optional[Surface] = None


    def _inner_init(self):

        self._winner_button = ViewButton(45, "P1 Win", disabled=True)
        self._winner_button.set_size(300, 100)
        self.add_child(self._winner_button)

        self._play_again_button = ViewButton(45, "Play Again!")
        self._play_again_button.set_size(200, 70)
        self._play_again_button.set_action_callback(self._shared_data.get_show_view_callback("color_select"))
        self.add_child(self._play_again_button)

        self._quit_button = ViewButton(20, "Quit")
        self._quit_button.set_size(100, 30)
        self._quit_button.set_action_callback(self._shared_data.get_show_view_callback("title"))
        self.add_child(self._quit_button)

        self._ko_text = self._shared_data.get_font(32).render("KOs", True, self.TEXT_COLOR)
        self._plants_collected_text = self._shared_data.get_font(32).render("Plants collected", True, self.TEXT_COLOR)
        self._damage_dealt_text = self._shared_data.get_font(32).render("Damage dealt", True, self.TEXT_COLOR)
        self._damage_taken_text = self._shared_data.get_font(32).render("Damage taken", True, self.TEXT_COLOR)

        self._ko_p1_text = self._shared_data.get_font(32).render("0", True, self.TEXT_COLOR)
        self._plants_collected_p1_text = self._shared_data.get_font(32).render("0", True, self.TEXT_COLOR)
        self._damage_dealt_p1_text = self._shared_data.get_font(32).render("0", True, self.TEXT_COLOR)
        self._damage_taken_p1_text = self._shared_data.get_font(32).render("0", True, self.TEXT_COLOR)

        self._ko_p2_text = self._shared_data.get_font(32).render("0", True, self.TEXT_COLOR)
        self._plants_collected_p2_text = self._shared_data.get_font(32).render("0", True, self.TEXT_COLOR)
        self._damage_dealt_p2_text = self._shared_data.get_font(32).render("0", True, self.TEXT_COLOR)
        self._damage_taken_p2_text = self._shared_data.get_font(32).render("0", True, self.TEXT_COLOR)

        self._ko_p3_text = self._shared_data.get_font(32).render("0", True, self.TEXT_COLOR)
        self._plants_collected_p3_text = self._shared_data.get_font(32).render("0", True, self.TEXT_COLOR)
        self._damage_dealt_p3_text = self._shared_data.get_font(32).render("0", True, self.TEXT_COLOR)
        self._damage_taken_p3_text = self._shared_data.get_font(32).render("0", True, self.TEXT_COLOR)

        self._ko_p4_text = self._shared_data.get_font(32).render("0", True, self.TEXT_COLOR)
        self._plants_collected_p4_text = self._shared_data.get_font(32).render("0", True, self.TEXT_COLOR)
        self._damage_dealt_p4_text = self._shared_data.get_font(32).render("0", True, self.TEXT_COLOR)
        self._damage_taken_p4_text = self._shared_data.get_font(32).render("0", True, self.TEXT_COLOR)

        self._player_anim_surface = self._shared_data.new_anim_colored("farmer", FARMER_ANIMATION, 210, 210)

    def _inner_pre_draw(self, surface: Surface):
        stage = self._shared_data.get_game().get_stage()
        players = stage.get_players()

        main_group_x = surface.get_width()/2
        surface_width, surface_height = surface.get_size()

        self._winner_button.set_position_centered(main_group_x, 75)
        self._play_again_button.set_position_centered(main_group_x, 700)
        self._quit_button.set_position_centered(80, 730)

        if len(players) >= 2 :

            # tableau 1
            pygame.draw.rect(surface, self.BUTTON_NORMAL_COLOR, (20, 150, 229, 252))

            pygame.draw.line(surface, self.TEXT_COLOR, (20, 150), (248, 150), 1)
            pygame.draw.line(surface, self.TEXT_COLOR, (20, 213), (248, 213), 1)
            pygame.draw.line(surface, self.TEXT_COLOR, (20, 276), (248, 276), 1)
            pygame.draw.line(surface, self.TEXT_COLOR, (20, 339), (248, 339), 1)
            pygame.draw.line(surface, self.TEXT_COLOR, (20, 402), (248, 402), 1)

            surface.blit(self._ko_text, (27, 171))
            surface.blit(self._plants_collected_text, (27, 234))
            surface.blit(self._damage_dealt_text, (27, 297))
            surface.blit(self._damage_taken_text, (27, 360))

            surface.blit(self._ko_p1_text, (217, 171))
            surface.blit(self._plants_collected_p1_text, (217, 234))
            surface.blit(self._damage_dealt_p1_text, (217, 297))
            surface.blit(self._damage_taken_p1_text, (217, 360))

            self._player_anim_surface.blit_color_on(surface, (25, 425), self._player_anim_tracker, (255, 0, 0))

            # tableau 2
            pygame.draw.rect(surface, self.BUTTON_NORMAL_COLOR, (270, 150, 229, 252))

            pygame.draw.line(surface, self.TEXT_COLOR, (270, 150), (498, 150), 1)
            pygame.draw.line(surface, self.TEXT_COLOR, (270, 213), (498, 213), 1)
            pygame.draw.line(surface, self.TEXT_COLOR, (270, 276), (498, 276), 1)
            pygame.draw.line(surface, self.TEXT_COLOR, (270, 339), (498, 339), 1)
            pygame.draw.line(surface, self.TEXT_COLOR, (270, 402), (498, 402), 1)

            surface.blit(self._ko_text, (274, 171))
            surface.blit(self._plants_collected_text, (274, 234))
            surface.blit(self._damage_dealt_text, (274, 297))
            surface.blit(self._damage_taken_text, (274, 360))

            surface.blit(self._ko_p2_text, (463, 171))
            surface.blit(self._plants_collected_p2_text, (463, 234))
            surface.blit(self._damage_dealt_p2_text, (463, 297))
            surface.blit(self._damage_taken_p2_text, (463, 360))

            self._player_anim_surface.blit_color_on(surface, (280, 425), self._player_anim_tracker, (255, 0, 0))

            if len(players) >= 3 :

                # tableau 3
                pygame.draw.rect(surface, self.BUTTON_NORMAL_COLOR, (520, 150, 229, 252))

                pygame.draw.line(surface, self.TEXT_COLOR, (520, 150), (748, 150), 1)
                pygame.draw.line(surface, self.TEXT_COLOR, (520, 213), (748, 213), 1)
                pygame.draw.line(surface, self.TEXT_COLOR, (520, 276), (748, 276), 1)
                pygame.draw.line(surface, self.TEXT_COLOR, (520, 339), (748, 339), 1)
                pygame.draw.line(surface, self.TEXT_COLOR, (520, 402), (748, 402), 1)

                surface.blit(self._ko_text, (527, 171))
                surface.blit(self._plants_collected_text, (527, 234))
                surface.blit(self._damage_dealt_text, (527, 297))
                surface.blit(self._damage_taken_text, (527, 360))

                surface.blit(self._ko_p3_text, (720, 171))
                surface.blit(self._plants_collected_p3_text, (720, 234))
                surface.blit(self._damage_dealt_p3_text, (720, 297))
                surface.blit(self._damage_taken_p3_text, (720, 360))

                self._player_anim_surface.blit_color_on(surface, (535, 425), self._player_anim_tracker, (255, 0, 0))

                if len(players) >= 4 :

                    # tableau 4
                    pygame.draw.rect(surface, self.BUTTON_NORMAL_COLOR, (770, 150, 229, 252))

                    pygame.draw.line(surface, self.TEXT_COLOR, (770, 150), (998, 150), 1)
                    pygame.draw.line(surface, self.TEXT_COLOR, (770, 213), (998, 213), 1)
                    pygame.draw.line(surface, self.TEXT_COLOR, (770, 276), (998, 276), 1)
                    pygame.draw.line(surface, self.TEXT_COLOR, (770, 339), (998, 339), 1)
                    pygame.draw.line(surface, self.TEXT_COLOR, (770, 402), (998, 402), 1)

                    surface.blit(self._ko_text, (777, 171))
                    surface.blit(self._plants_collected_text, (777, 234))
                    surface.blit(self._damage_dealt_text, (777, 297))
                    surface.blit(self._damage_taken_text, (777, 360))

                    surface.blit(self._ko_p4_text, (970, 171))
                    surface.blit(self._plants_collected_p4_text, (970, 234))
                    surface.blit(self._damage_dealt_p4_text, (970, 297))
                    surface.blit(self._damage_taken_p4_text, (970, 360))

                    self._player_anim_surface.blit_color_on(surface, (790, 425), self._player_anim_tracker, (255, 0, 0))

            cmpt = 0
            for idx, player in players.items():
                if cmpt == 0:
                    self._player_anim_surface.blit_color_on(surface, (25, 425), self._player_anim_tracker,(get_player_color(player.get_color())))
                    cmpt = cmpt + 1
                elif cmpt == 1:
                    self._player_anim_surface.blit_color_on(surface, (280, 425), self._player_anim_tracker,(get_player_color(player.get_color())))
                    cmpt = cmpt + 1
                elif cmpt == 2:
                    self._player_anim_surface.blit_color_on(surface, (535, 425), self._player_anim_tracker,(get_player_color(player.get_color())))
                    cmpt = cmpt + 1
                elif cmpt == 3:
                    self._player_anim_surface.blit_color_on(surface, (790, 425), self._player_anim_tracker,(get_player_color(player.get_color())))
                    cmpt = cmpt + 1

                pass

    def on_enter(self):

        self._winner_button.set_text("P" + str(self._shared_data.get_game().get_stage().get_winner().get_player_index() + 1) + " Win!")

        stage = self._shared_data.get_game().get_stage()
        players = stage.get_players()
        cmpt = 0
        for idx, player in players.items():
            if cmpt == 0:
                self._ko_p1_text = self._shared_data.get_font(32).render(str(player.get_statistics().get_kos()), True, self.TEXT_COLOR)
                self._plants_collected_p1_text = self._shared_data.get_font(32).render(str(player.get_statistics().get_plants_collected()), True, self.TEXT_COLOR)
                self._damage_dealt_p1_text = self._shared_data.get_font(32).render(str(player.get_statistics().get_damage_dealt()), True, self.TEXT_COLOR)
                self._damage_taken_p1_text = self._shared_data.get_font(32).render(str(player.get_statistics().get_damage_taken()), True, self.TEXT_COLOR)
                cmpt = cmpt + 1
            elif cmpt == 1:
                self._ko_p2_text = self._shared_data.get_font(32).render(str(player.get_statistics().get_kos()), True, self.TEXT_COLOR)
                self._plants_collected_p2_text = self._shared_data.get_font(32).render(str(player.get_statistics().get_plants_collected()), True, self.TEXT_COLOR)
                self._damage_dealt_p2_text = self._shared_data.get_font(32).render(str(player.get_statistics().get_damage_dealt()), True, self.TEXT_COLOR)
                self._damage_taken_p2_text = self._shared_data.get_font(32).render(str(player.get_statistics().get_damage_taken()), True, self.TEXT_COLOR)
                cmpt = cmpt + 1
            elif cmpt == 2:
                self._ko_p3_text = self._shared_data.get_font(32).render(str(player.get_statistics().get_kos()), True, self.TEXT_COLOR)
                self._plants_collected_p3_text = self._shared_data.get_font(32).render(str(player.get_statistics().get_plants_collected()), True, self.TEXT_COLOR)
                self._damage_dealt_p3_text = self._shared_data.get_font(32).render(str(player.get_statistics().get_damage_dealt()), True, self.TEXT_COLOR)
                self._damage_taken_p3_text = self._shared_data.get_font(32).render(str(player.get_statistics().get_damage_taken()), True, self.TEXT_COLOR)
                cmpt = cmpt + 1
            elif cmpt == 3:
                self._ko_p4_text = self._shared_data.get_font(32).render(str(player.get_statistics().get_kos()), True, self.TEXT_COLOR)
                self._plants_collected_p4_text = self._shared_data.get_font(32).render(str(player.get_statistics().get_plants_collected()), True, self.TEXT_COLOR)
                self._damage_dealt_p4_text = self._shared_data.get_font(32).render(str(player.get_statistics().get_damage_dealt()), True, self.TEXT_COLOR)
                self._damage_taken_p4_text = self._shared_data.get_font(32).render(str(player.get_statistics().get_damage_taken()), True, self.TEXT_COLOR)
                cmpt = cmpt + 1
