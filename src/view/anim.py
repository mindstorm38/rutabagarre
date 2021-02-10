from typing import Dict, Tuple, List, Optional, Any
import time

from pygame import Surface
import pygame

from .tilemap import GridDefinition


def _format_reversed(name: str, rev: bool) -> str:
    return "{}_rev".format(name) if rev else name


class AnimDefinition(GridDefinition):

    __slots__ = "animations",

    def __init__(self, x_pad: int, y_pad: int, x_gap: int, y_gap: int, tile_width: int, tile_height: int):
        super().__init__(x_pad, y_pad, x_gap, y_gap, tile_width, tile_height)
        self.animations: Dict[str, Tuple[Tuple[int, int, int], ...]] = {}

    def animation(self, name: str, *ranges: Tuple[int, int, int]) -> 'AnimDefinition':

        """
        Ajoute une animation nommée. Une liste de toutes les intervalles de tuiles doit être donné, chaque intervalle
        est défini comme le tuple suivant: `(x, y, count)` avec `x/y` la position de la tuile d'origine avec `0/0`
        étant la tuile la plus en haut à gauche. Le champs `count` contient le nombre de tuiles consécutive. **Au
        final toutes ces intervalles sont concaténées à l'affichage.**
        """

        if len(ranges) == 0:
            raise ValueError("An animation can't be empty.")

        self.animations[name] = ranges
        return self


class Anim:

    __slots__ = "surface", "definition", "sub_surfaces"

    def __init__(self, surface: Surface, definition: AnimDefinition, *, no_init: bool = False):

        self.surface = surface
        self.definition = definition
        self.sub_surfaces: Dict[str, List[Surface]] = {}

        if not no_init:
            for name, ranges in definition.animations.items():
                for rev in (False, True):
                    self.sub_surfaces[_format_reversed(name, rev)] = sub_surfaces = []
                    for x, y, count in ranges:
                        for _ in range(count):
                            px, py = definition.get_tile_pos(x, y)
                            sub_surface = surface.subsurface(px, py, definition.tile_width, definition.tile_height)
                            if rev:
                                sub_surface = pygame.transform.flip(sub_surface, True, False)
                            sub_surfaces.append(sub_surface)
                            x += 1

    def copy_scaled(self, width: int, height: int) -> 'Anim':
        new_anim = Anim(self.surface, self.definition, no_init=True)
        for name, frames in self.sub_surfaces.items():
            new_anim.sub_surfaces[name] = [pygame.transform.scale(frame, (width, height)) for frame in frames]
        return new_anim

    def mul_color(self, color: Tuple[int, int, int]):
        for name, frames in self.sub_surfaces.items():
            for frame in frames:
                frame.fill(color, special_flags=pygame.BLEND_RGBA_MULT)


class AnimTracker:

    __slots__ = "_anims_queue", "_last_time", "_last_anim_name"

    def __init__(self):
        self._last_anim_name: Optional[str] = None
        self._anims_queue = []
        self._last_time = 0

    def push_anim(self, name: str, repeat_count: int, fps: float, *, rev: bool = False, ignore_existing: bool = True):

        """
        Ajoute une animation dans la queue des animation.

        :param name: Nom de l'animation à jouer.
        :param repeat_count: Si < 1 l'animation va être stoppé instantanément, si == 0 la durée est indéfini,
         sinon c'est le nombre de fois qu'il faut jouer l'animation.
        :param fps: Nombre d'image par secondes.
        :param rev: Prendre ou non l'animation renversé sur l'axe X.
        :param ignore_existing: Mettre à `False` si on ne veut pas ajouter l'animation si on a déjà la même
         avant (suivant `name`).
        """

        if ignore_existing or self._last_anim_name != name:
            self._last_anim_name = name
            self._anims_queue.insert(0, [name, _format_reversed(name, rev), repeat_count, 1 / fps, 0, rev])
            # base name, effective name, repeat count, interval, reversed?

    def push_infinite_anim(self, name: str, fps: float, *, rev: bool = False, ignore_existing: bool = True):
        """ Version raccourci de `push_anim` avec un `repeat_count = 0` (durée indeterminée). """
        self.push_anim(name, 0, fps, rev=rev, ignore_existing=ignore_existing)

    def stop_last_anim(self, name: str):

        """
        Défini le `repeat_count = -1` (arrêt de l'animation) de la dernière anim demandée si
        celle-ci est bien nommée `name`.
        """

        if self._last_anim_name == name:
            self._anims_queue[0][2] = -1

    def set_all_reversed(self, rev: bool):
        for data in self._anims_queue:
            data[1] = _format_reversed(data[0], rev)

    def get_anim(self) -> Optional[Tuple[str, int, int]]:

        if not len(self._anims_queue):
            return None

        data = self._anims_queue[0]

        now = time.monotonic()
        if now - self._last_time >= data[3]:
            if self._last_time != 0:
                data[4] += 1
            self._last_time = now

        # tile name, frames count, repeat count
        return data[1], data[4], data[2]

    def pop_anim(self):
        if len(self._anims_queue):
            self._anims_queue.pop(0)
        self._last_anim_name = self._anims_queue[0][0] if len(self._anims_queue) else None


class _AnimLayer:

    __slots__ = "raw_anim", "anim"

    def __init__(self, raw_anim: Anim):
        self.raw_anim = raw_anim
        self.anim: Optional[Anim] = None

    def rescale_lazy(self, width: int, height: int):
        if self.anim is None:
            self._rescale(width, height)

    def _rescale(self, width: int, height: int):
            self.anim = self.raw_anim.copy_scaled(width, height)


class AnimSurface:

    __slots__ = "_width", "_height", "_layers"

    def __init__(self, width: int, height: int, layers: List[Anim]):
        self._width = width
        self._height = height
        self._layers: List[_AnimLayer] = [_AnimLayer(anim) for anim in layers]

    def add_layer(self, anim: Anim):
        self._layers.append(_AnimLayer(anim))

    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height

    def get_size(self) -> Tuple[int, int]:
        return self._width, self._height

    # Private #

    def _rescale_lazy_layers(self):
        for layer in self._layers:
            layer.rescale_lazy(self._width, self._height)

    def _get_layer(self, layer_idx: Any) -> _AnimLayer:
        return self._layers[layer_idx]

    # Méthodes override #

    def blit_on(self, surface: Surface, pos: Tuple[int, int], tracker: AnimTracker, *, layers: Optional[tuple] = None):
        for layer in (self._layers if layers is None else map(self._get_layer, layers)):
            layer.rescale_lazy(self._width, self._height)
            anim = tracker.get_anim()
            if anim is not None:
                anim_name, frame, repeat_count = anim
                sub_surfaces = layer.anim.sub_surfaces.get(anim_name)
                sub_surfaces_count = len(sub_surfaces)
                sub_surface = sub_surfaces[frame % sub_surfaces_count]
                surface.blit(sub_surface, pos)
                if repeat_count != 0 or 0 < repeat_count < (frame // sub_surfaces_count):
                    tracker.pop_anim()


class _AnimLayerColored(_AnimLayer):

    __slots__ = "color"

    def __init__(self, raw_anim: Anim, color: Tuple[int, int, int]):
        super().__init__(raw_anim)
        self.color = color

    def _rescale(self, width: int, height: int):
        super()._rescale(width, height)
        self.anim.mul_color(self.color)


class AnimSurfaceColored(AnimSurface):

    def __init__(self, width: int, height: int, main_anim: Anim, overlay_anim: Anim):
        super().__init__(width, height, [main_anim])
        self._colors_indices: Dict[int, int] = {}
        self._overlay_anim = overlay_anim

    def blit_color_on(self, surface: Surface, pos: Tuple[int, int], tracker: AnimTracker, color: Tuple[int, int, int]):
        self.blit_on(surface, pos, tracker, layers=(0, color))

    def _get_layer(self, layer_idx: Any) -> _AnimLayer:
        if layer_idx == 0:
            return super()._get_layer(layer_idx)
        else:
            color_index = self._color_to_index(layer_idx)
            index = self._colors_indices.get(color_index)
            if index is None:
                index = len(self._layers)
                self._colors_indices[color_index] = index
                layer = _AnimLayerColored(self._overlay_anim, layer_idx)
                self._layers.append(layer)
                return layer
            else:
                return super()._get_layer(index)

    @staticmethod
    def _color_to_index(color: Tuple[int, int, int]) -> int:
        return color[2] << 16 | color[1] << 8 | color[0]


FARMER_ANIMATION = AnimDefinition(1, 1, 1, 1, 30, 30)\
    .animation("idle", (0, 0, 5))\
    .animation("hit", (6, 0, 3))\
    .animation("walk", (0, 1, 7))\
    .animation("jump", (1, 2, 3))\
    .animation("pick", (5, 2, 5))\
    .animation("run_med", (1, 3, 6))\
    .animation("run", (1, 4, 6)) \
    .animation("grab", (1, 5, 10), (1, 6, 11))\
    .animation("attack_side", (1, 7, 5))\
    .animation("attack_up", (1, 9, 6))\
    .animation("attack_down", (1, 10, 9))\
    .animation("air_attack_side", (1, 11, 5))\
    .animation("air_attack_up", (1, 12, 6))\
    .animation("air_attack_down", (1, 13, 9))
