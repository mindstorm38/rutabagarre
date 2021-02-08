from abc import ABC, abstractmethod
from typing import Optional, Dict

from pygame.font import Font
from pygame import Surface
import pygame

import res


class View(ABC):

    """
    Une classe abstraite pour toutes les vues enregistrées dans le jeu.
    """

    @abstractmethod
    def init(self, data: 'CommonViewData'):
        """ Appelée à l'initialisation du jeu avec les données communes des vues. """

    @abstractmethod
    def draw(self, surface: Surface):
        """ Appelée à chaque image, doit dessiner la vue. """


class CommonViewData:

    """
    Données commune à toutes les vues, permettant pour l'instant de cacher
    les fontes pour éviter de les recharger.
    """

    def __init__(self):
        self._fonts: Dict[int, Font] = {}

    def init(self):
        """ Appelée lors de l'initialisation du jeu, après la création de la fenêtre. """

    def cleanup(self):
        """ Appelée à la fermeture du jeu afin de supprimer les données désormais invalide. """
        self._fonts = {}

    def get_font(self, size: int) -> Font:

        """
        Récupère une fonte suivant la taille donnée, la fonte n'est pas recréée si elle a déjà été chargée.
        """

        font = self._fonts.get(size)
        if font is None:
            font = Font(res.get_res("5x7-practical-regular.ttf"), size)
            self._fonts[size] = font
        return font


class Button:

    """
    Bouton pouvant être utilisé par les vues, doit être créé dans `View.init` au plus tôt en
    fournissant la fonte et le texte. Il faut également définir sa position et sa taille.
    """

    BUTTON_FONT_COLOR = (255, 255, 255)
    BUTTON_BACKGROUND_COLOR = (133, 43, 24)

    def __init__(self, font: Font, text: str):

        if font is None or text is None:
            raise ValueError("Font and text can't be None.")

        self._font = font
        self._text = text
        self._pos = (0, 0)
        self._size = (300, 50)

        self._text_surface: Optional[Surface] = None
        self._text_pos = (0, 0)
        self._redraw()

    def _redraw(self):
        self._text_surface = self._font.render(self._text, True, self.BUTTON_FONT_COLOR, self.BUTTON_BACKGROUND_COLOR)
        self._refresh_text_pos()

    def _refresh_text_pos(self):
        rect = self._text_surface.get_rect()
        self._text_pos = (
            self._pos[0] + (self._size[0] - rect.width) / 2,
            self._pos[1] + (self._size[1] - rect.height) / 2
        )

    def set_position(self, x: float, y: float):
        self._pos = (x, y)
        self._refresh_text_pos()

    def set_size(self, width: float, height: float):
        self._size = (width, height)
        self._refresh_text_pos()

    def set_position_centered(self, x: float, y: float):
        self.set_position(x - self._size[0] / 2, y - self._size[1] / 2)

    def draw(self, surface: Surface):
        pygame.draw.rect(surface, self.BUTTON_BACKGROUND_COLOR, self._pos + self._size, 0, 5)
        surface.blit(self._text_surface, self._text_pos)
