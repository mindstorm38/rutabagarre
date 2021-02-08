from abc import ABC, abstractmethod
from typing import Dict, List

from pygame.event import Event
from pygame.font import Font
from pygame import Surface

import game
import res


class View(ABC):

    """
    Une classe abstraite pour toutes les vues enregistrées dans le jeu.
    """

    BACKGROUND_COLOR = (54, 16, 12)

    def __init__(self):
        self._children: List['ViewObject'] = []

    def add_child(self, child: 'ViewObject'):
        self._children.append(child)

    @abstractmethod
    def init(self, data: 'SharedViewData'):
        """ Appelée à l'initialisation du jeu avec les données communes des vues. """

    def draw(self, surface: Surface):

        """ Appelée à chaque image, doit dessiner la vue sur la `surface` donnée. """

        surface.fill(self.BACKGROUND_COLOR)

        for child in self._children:
            child.draw(surface)

    def event(self, event: Event):
        """ Appelée pour chaque évènement PyGame. """
        for child in self._children:
            child.event(event)


class SharedViewData:

    """
    Données commune à toutes les vues, permettant pour l'instant de cacher
    les fontes pour éviter de les recharger.
    """

    def __init__(self, the_game: 'game.Game'):
        self._game = the_game
        self._fonts: Dict[int, Font] = {}

    def init(self):
        """ Appelée lors de l'initialisation du jeu, après la création de la fenêtre. """

    def cleanup(self):
        """ Appelée à la fermeture du jeu afin de supprimer les données désormais invalide. """
        self._fonts = {}

    def get_game(self) -> 'game.Game':
        """ Retourne l'instance actuelle du controlleur de jeu. """
        return self._game

    def get_font(self, size: int) -> Font:
        """ Récupère une fonte suivant la taille donnée, la fonte n'est pas recréée si elle a déjà été chargée. """
        font = self._fonts.get(size)
        if font is None:
            font = Font(res.get_res("5x7-practical-regular.ttf"), size)
            self._fonts[size] = font
        return font

    def get_show_view_callback(self, view_name: str) -> callable:
        """ Retourne une fonction de type `callback` qui change la vue active quand elle est appelée. """
        def _cb(*_args, **_kwargs):
            self._game.show_view(view_name)
        return _cb


class ViewObject(ABC):

    def __init__(self, width: float, height: float):
        self._pos = (0, 0)
        self._size = (0, 0)

    @abstractmethod
    def draw(self, surface: Surface):
        """ Appelée à chaque frame pour afficher cet objet. """

    @abstractmethod
    def event(self, event: Event):
        """ Appelée pour chaque évènement PyGame. """

    def set_position(self, x: float, y: float):
        self._pos = (x, y)

    def set_size(self, width: float, height: float):
        self._size = (width, height)

    def set_position_centered(self, x: float, y: float):
        self.set_position(x - self._size[0] / 2, y - self._size[1] / 2)

    def is_cursor_over(self, mx: float, my: float):
        x, y = self._pos
        width, height = self._size
        return x <= mx <= x + width and y <= my <= y + height
