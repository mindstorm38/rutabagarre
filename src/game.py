from typing import Optional, Dict
from pygame import Surface
import pygame

from stage import Stage
from view import View, SharedViewData
from view.title import TitleView


class Game:

    """
    Classe principale pour le jeu. A le rôle du controlleur et possède les
    instances du Stage en cours d'execution ainsi que les vues.
    """

    def __init__(self):

        self._surface: Optional[Surface] = None
        self._running: bool = False

        self._views: Dict[str, View] = {}
        self._active_view: Optional[View] = None
        self._view_data = SharedViewData()

        self._stage: Optional[Stage] = None

        self._init_views()

    def _init_views(self):

        """
        Ajout de toutes les vues (à compléter au fur et à mesure).
        """

        self._add_view("title", TitleView())

    def start(self):

        """
        Point d'entrée pour le jeu.
        """

        print("=> Starting PyGame...")

        pygame.init()
        self._surface = pygame.display.set_mode((1024, 768))
        self._running = True

        print("=> Initializing views...")

        self._view_data.init()
        for view in self._views.values():
            view.init(self._view_data)

        self.show_view("title")

        print("=> Start loop...")

        while self._running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

            self._update()

            pygame.display.flip()

        print("=> Cleanup...")

        self._view_data.cleanup()
        self._surface = None
        self._stage = None
        self._active_view = None
        pygame.quit()

        print("=> Game stopped.")

    def _update(self):

        """
        Appelé à chaque frame afin de mettre à jour l'affichage et la physique.
        """

        if self._stage is not None:
            self._stage.update()

        if self._active_view is not None:
            self._active_view.draw(self._surface)

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
        self._active_view = view
