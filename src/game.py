from typing import Optional, Dict
from pygame.time import Clock
from pygame import Surface
import pygame
import time

from stage import Stage
from view import View, SharedViewData
from view.kind import *
import res


class Game:

    """
    Classe principale pour le jeu. A le rôle du contrôleur et possède les
    instances du Stage en cours d'exécution ainsi que les vues.
    """

    DEBUG_PERFS = False

    def __init__(self):

        self._surface: Optional[Surface] = None
        self._running: bool = False

        self._views: Dict[str, View] = {}
        self._active_view: Optional[View] = None
        self._view_data = SharedViewData(self)

        self._stage: Optional[Stage] = None

        self._perf_update: float = 0
        self._perf_draw: float = 0
        self._next_perf_print: float = 0

        self._init_views()

    def _init_views(self):

        """
        Ajout de toutes les vues (à compléter au fur et à mesure).
        """

        self._add_view("title", TitleView())
        self._add_view("color_select", ColorSelectView())
        self._add_view("in_game", InGameView())
        self._add_view("credits", CreditsView())
        self._add_view("scenario", ScenarioView())
        self._add_view("end", EndView())
        self._add_view("how_to_play", HowToPlayView())
        self._add_view("settings", SettingsView())

    def start(self):

        """
        Point d'entrée pour le jeu.
        """

        print()
        print("[GAME] Starting PyGame...")

        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Rutabagarre")
        pygame.display.set_icon(pygame.image.load(res.get_res("menusmisc/favicon32.png")))

        self._surface = pygame.display.set_mode((1024, 768))
        self._running = True

        print("[GAME] Initializing views...")

        self._view_data.init()
        for view in self._views.values():
            view.init(self._view_data)

        self.show_view("scenario")

        print("[GAME] Start loop...")

        clock = Clock()

        while self._running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                elif self._active_view is not None:
                    self._active_view.event(event)

            self._update()

            pygame.display.flip()
            clock.tick(60)

        print("[GAME] Cleanup...")

        self._view_data.cleanup()
        self._surface = None
        self._stage = None
        self._active_view = None
        pygame.quit()

        print("[GAME] Stopped.")

    def _update(self):

        """
        Appelé à chaque frame afin de mettre à jour l'affichage et la physique.
        """

        if self._stage is not None:
            start = time.perf_counter_ns()
            self._stage.update()
            self._perf_update = time.perf_counter_ns() - start

        if self._active_view is not None:
            start = time.perf_counter_ns()
            self._active_view.draw(self._surface)
            self._perf_draw = time.perf_counter_ns() - start

        if self.DEBUG_PERFS and time.monotonic() >= self._next_perf_print:
            self._next_perf_print = time.monotonic() + 2.0
            print("Timings: Update: {}ns, Draw: {}ns".format(self._perf_update, self._perf_draw))

    def _add_view(self, name: str, view: View):

        """
        Ajoute une vue associée à son nom, utile plus tard pour `show_view`.
        :param name: Nom de la vue.
        :param view: Instance de la vue.
        """

        if name is None or view is None:
            raise ValueError("Name and view object can't be None.")
        self._views[name] = view

    def show_view(self, view_name: str):

        """
        Défini la nouvelle vue à afficher en fonction de son nom lors de
        son enregistrement.
        """

        view = self._views.get(view_name)
        if view is None:
            raise ValueError("Invalid view name '{}'.".format(view_name))

        if self._active_view is not None:
            self._active_view.on_quit()

        print("[GAME] Show view: {}".format(view_name))
        self._active_view = view
        view.on_enter()

    def get_surface(self) -> Optional[Surface]:
        return self._surface

    def get_stage(self) -> Stage:
        return self._stage

    def set_stage(self, stage: Stage):
        self._stage = stage

    def remove_stage(self):
        self._stage = None

    def stop_game(self):
        self._running = False
