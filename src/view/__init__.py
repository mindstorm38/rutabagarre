from typing import Dict, List, Optional
from abc import ABC, abstractmethod

from pygame.event import Event
from pygame.font import Font
from pygame import Surface
import pygame

from view.anim import AnimDefinition, Anim, AnimSurfaceColored
from view.tilemap import TileMap, TileMapDefinition
import game
import res


class View(ABC):

    """
    Une classe abstraite pour toutes les vues enregistrées dans le jeu.
    """

    BACKGROUND_COLOR    = 133, 43, 24
    BUTTON_NORMAL_COLOR = 54, 16, 12
    BUTTON_OVER_COLOR   = 69, 20, 15
    TEXT_COLOR          = 255, 255, 255

    def __init__(self):
        self._children: List['ViewObject'] = []
        self._shared_data: Optional['SharedViewData'] = None

    def add_child(self, child: 'ViewObject'):
        self._children.append(child)
        child.set_view(self)

    def get_shared_data(self) -> Optional['SharedViewData']:
        return self._shared_data

    def init(self, data: 'SharedViewData'):
        """ Appelée à l'initialisation du jeu avec les données communes des vues. """
        self._shared_data = data
        self._inner_init()

    def draw(self, surface: Surface):
        """ Appelée à chaque image, doit dessiner la vue sur la `surface` donnée. """
        if self.BACKGROUND_COLOR is not None:
            surface.fill(self.BACKGROUND_COLOR)
        self._inner_pre_draw(surface)
        for child in self._children:
            if child.is_visible():
                child.draw(surface)

    def on_enter(self): ...
    def on_quit(self): ...

    @abstractmethod
    def _inner_init(self): ...

    @abstractmethod
    def _inner_pre_draw(self, surface: Surface): ...

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
        self._images: Dict[str, Surface] = {}
        self._animations: Dict[str, Anim] = {}
        self._tilemaps: Dict[str, TileMap] = {}

    def init(self):
        """ Appelée lors de l'initialisation du jeu, après la création de la fenêtre. """

    def cleanup(self):
        """ Appelée à la fermeture du jeu afin de supprimer les données désormais invalide. """
        self._fonts.clear()
        self._images.clear()
        self._animations.clear()
        self._tilemaps.clear()

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

    def get_image(self, res_path: str) -> Surface:
        image = self._images.get(res_path)
        if image is None:
            image = pygame.image.load(res.get_res(res_path))
            self._images[res_path] = image
        return image

    def get_anim(self, res_path: str, anim_def: AnimDefinition) -> Anim:
        animation = self._animations.get(res_path)
        if animation is None:
            animation = Anim(self.get_image(res_path), anim_def)
            self._animations[res_path] = animation
        elif animation.definition != anim_def:
            raise ValueError("The animation for '{}' is already set but not of this type.".format(res_path))
        return animation

    def get_tilemap(self, res_path: str, map_def: TileMapDefinition) -> TileMap:
        tm = self._tilemaps.get(res_path)
        if tm is None:
            tm = TileMap(self.get_image(res_path), map_def)
            self._tilemaps[res_path] = tm
        elif tm.definition != map_def:
            raise ValueError("The tile map for '{}' is already set but not of this type.".format(res_path))
        return tm

    def new_anim_colored(self, anim_name, anim_def: AnimDefinition, width: int, height: int) -> AnimSurfaceColored:
        main_anim = self.get_anim("animations/{}.png".format(anim_name), anim_def)
        overlay_anim = self.get_anim("animations/{}_overlay.png".format(anim_name), anim_def)
        return AnimSurfaceColored(width, height, main_anim, overlay_anim)

    def get_show_view_callback(self, view_name: str) -> callable:
        """ Retourne une fonction de type `callback` qui change la vue active quand elle est appelée. """
        def _cb(*_args, **_kwargs):
            self._game.show_view(view_name)
        return _cb


class ViewObject(ABC):

    def __init__(self, width: float, height: float):
        self._view: Optional[View] = None
        self._pos = (0, 0)
        self._size = (width, height)
        self._visible = True

    @abstractmethod
    def draw(self, surface: Surface):
        """ Appelée à chaque frame pour afficher cet objet. """

    @abstractmethod
    def event(self, event: Event):
        """ Appelée pour chaque évènement PyGame. """

    def set_view(self, view: View):
        """ Appelée quand l'élément est ajouté à une vue. Permet notament de prendre en compte le thème. """
        self._view = view

    def set_position(self, x: float, y: float):
        self._pos = (x, y)
        self._on_shape_changed()

    def set_size(self, width: float, height: float):
        self._size = (width, height)
        self._on_shape_changed()

    def set_position_centered(self, x: float, y: float):
        self.set_position(x - self._size[0] / 2, y - self._size[1] / 2)

    def is_cursor_over(self, mx: float, my: float):
        x, y = self._pos
        width, height = self._size
        return x <= mx <= x + width and y <= my <= y + height

    def in_view(self) -> bool:
        return self._view is not None

    def get_width(self) -> float:
        return self._size[0]

    def get_height(self) -> float:
        return self._size[1]

    def set_visible(self, visible: bool):
        self._visible = visible

    def is_visible(self) -> bool:
        return self._visible

    # Private / Protected #

    def _get_font(self, size: int) -> Optional[Font]:
        return None if self._view is None else self._view.get_shared_data().get_font(size)

    def _on_shape_changed(self):
        pass