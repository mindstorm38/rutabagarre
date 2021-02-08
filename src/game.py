from typing import Optional, Dict
from pygame import Surface
import pygame

from stage import Stage
from view import View, CommonViewData
from view.title import TitleView


class Game:

    def __init__(self):

        self._surface: Optional[Surface] = None
        self._running: bool = False

        self._views: Dict[str, View] = {}
        self._view: Optional[View] = None
        self._view_data = CommonViewData()

        self._stage: Optional[Stage] = None

        self.init_views()

    def init_views(self):
        self._add_view("title", TitleView())

    def show_view(self, view_name: str):
        view = self._views.get(view_name)
        if view is None:
            raise ValueError("Invalid view name '{}'.".format(view_name))
        self._view = view

    def start(self):

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
        pygame.quit()

        print("=> Game stopped.")

    def _update(self):

        if self._stage is not None:
            self._stage.update()

        if self._view is not None:
            self._view.draw(self._surface)

    def _add_view(self, name: str, view: View):
        if name is None or view is None:
            raise ValueError("Name and view object can't be None.")
        self._views[name] = view
