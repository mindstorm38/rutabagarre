from typing import Dict, Tuple, List, Optional, Any
import time

import pygame
from pygame import Surface


class AnimDefinition:

    __slots__ = "x_pad", "y_pad", "x_gap", "y_gap", "tile_width", "tile_height", "animations"

    def __init__(self, x_pad: int, y_pad: int, x_gap: int, y_gap: int, tile_width: int, tile_height: int):

        self.x_pad = x_pad
        self.y_pad = y_pad
        self.x_gap = x_gap
        self.y_gap = y_gap
        self.tile_width = tile_width
        self.tile_height = tile_height
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
                self.sub_surfaces[name] = sub_surfaces = []
                for x, y, count in ranges:
                    for _ in range(count):
                        px = definition.x_pad + x * (definition.x_gap + definition.tile_width)
                        py = definition.y_pad + y * (definition.y_gap + definition.tile_width)
                        sub_surfaces.append(surface.subsurface(px, py, definition.tile_width, definition.tile_height))
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

    __slots__ = "_anims_queue", "_last_time"

    def __init__(self):
        self._anims_queue = []
        self._last_time = 0

    def push_anim(self, name: str, repeat_count: int, fps: float):
        self._anims_queue.insert(0, [name, repeat_count, 1 / fps, 0])

    def push_infinite_anim(self, name: str, fps: float):
        self.push_anim(name, 0, fps)

    def get_anim(self) -> Optional[Tuple[str, int, int]]:

        if not len(self._anims_queue):
            return None

        data = self._anims_queue[0]

        now = time.monotonic()
        if now - self._last_time >= data[2]:
            if self._last_time != 0:
                data[3] += 1
            self._last_time = now

        return data[0], data[3], data[1]

    def pop_anim(self):
        if len(self._anims_queue):
            self._anims_queue.pop(0)


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

    __slots__ = "_width", "_height", "_layers" # , "_delay", "_last_time", "_frame"

    def __init__(self, width: int, height: int, layers: List[Anim]):

        self._width = width
        self._height = height

        self._layers: List[_AnimLayer] = [_AnimLayer(anim) for anim in layers]
        # self._delay = 0.1
        # self._last_time = 0
        # self._frame = 0

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

        """now = time.monotonic()
        if now - self._last_time >= self._delay:
            self._last_time = now
            self._frame += 1"""

        for layer in (self._layers if layers is None else map(self._get_layer, layers)):
            layer.rescale_lazy(self._width, self._height)
            anim = tracker.get_anim()
            if anim is not None:
                anim_name, frame, repeat_count = anim
                sub_surfaces = layer.anim.sub_surfaces.get(anim_name)
                sub_surfaces_count = len(sub_surfaces)
                sub_surface = sub_surfaces[frame % sub_surfaces_count]
                surface.blit(sub_surface, pos)
                if 0 < repeat_count < (frame // sub_surfaces_count):
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
