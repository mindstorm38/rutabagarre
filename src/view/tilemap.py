from typing import Tuple, Dict, List, Optional
from abc import ABC

from pygame import Surface
import pygame


class GridDefinition(ABC):

    __slots__ = "x_pad", "y_pad", "x_gap", "y_gap", "tile_width", "tile_height"

    def __init__(self, x_pad: int, y_pad: int, x_gap: int, y_gap: int, tile_width: int, tile_height: int):

        self.x_pad = x_pad
        self.y_pad = y_pad
        self.x_gap = x_gap
        self.y_gap = y_gap
        self.tile_width = tile_width
        self.tile_height = tile_height

    def get_tile_pos(self, x: int, y: int) -> Tuple[int, int]:
        return (
            self.x_pad + x * (self.x_gap + self.tile_width),
            self.y_pad + y * (self.y_gap + self.tile_height)
        )


class TileMapDefinition(GridDefinition):

    __slots__ = "tiles",

    def __init__(self, x_pad: int, y_pad: int, x_gap: int, y_gap: int, tile_width: int, tile_height: int):
        super().__init__(x_pad, y_pad, x_gap, y_gap, tile_width, tile_height)
        self.tiles: Dict[str, Tuple[int, int]] = {}

    def tile(self, name: str, x: int, y: int) -> 'TileMapDefinition':
        self.tiles[name] = (x, y)
        return self


class TileMap:

    __slots__ = "surface", "definition", "sub_surfaces"

    def __init__(self, surface: Surface, definition: TileMapDefinition, *, no_init: bool = False):

        self.surface = surface
        self.definition = definition
        self.sub_surfaces: Dict[str, Surface] = {}

        if not no_init:
            for name, (x, y) in definition.tiles.items():
                px, py = definition.get_tile_pos(x, y)
                self.sub_surfaces[name] = surface.subsurface(px, py, definition.tile_width, definition.tile_height)

    def get_tile(self, name: str) -> Optional[Surface]:
        return self.sub_surfaces.get(name)

    def copy_scaled(self, width: int, height: int) -> 'TileMap':
        new_anim = TileMap(self.surface, self.definition, no_init=True)
        for name, surface in self.sub_surfaces.items():
            new_anim.sub_surfaces[name] = pygame.transform.scale(surface, (width, height))
        return new_anim


TERRAIN_TILEMAP = TileMapDefinition(0, 0, 1, 1, 16, 16)\
    .tile("TILE_DIRT_1", 2, 0)\
    .tile("TILE_DIRT_2", 3, 0)\
    .tile("TILE_DIRT_3", 4, 0)\
    .tile("TILE_DIRT_4", 2, 1)\
    .tile("TILE_DIRT_5", 3, 1)\
    .tile("TILE_DIRT_6", 4, 1)\
    .tile("TILE_DIRT_7", 2, 2)\
    .tile("TILE_DIRT_8", 3, 2)\
    .tile("TILE_DIRT_9", 4, 2)\
    .tile("TILE_GRASS_LIGHT_1", 5, 0)\
    .tile("TILE_GRASS_LIGHT_2", 6, 0)\
    .tile("TILE_GRASS_LIGHT_3", 7, 0)\
    .tile("TILE_GRASS_LIGHT_4", 5, 1)\
    .tile("TILE_GRASS_LIGHT_6", 7, 1)\
    .tile("TILE_GRASS_LIGHT_7", 5, 2)\
    .tile("TILE_GRASS_LIGHT_8", 6, 2)\
    .tile("TILE_GRASS_LIGHT_9", 7, 2)\
    .tile("TILE_GRASS_DARK_1", 8, 1)\
    .tile("TILE_GRASS_DARK_2", 9, 1)\
    .tile("TILE_GRASS_DARK_3", 10, 1)\
    .tile("TILE_GRASS_DARK_4", 8, 2)\
    .tile("TILE_GRASS_DARK_6", 10, 2)\
    .tile("TILE_GRASS_DARK_7", 8, 3)\
    .tile("TILE_GRASS_DARK_8", 9, 3)\
    .tile("TILE_GRASS_DARK_9", 10, 3)\
    .tile("TILE_FARMLAND", 0, 0)\
    .tile("TILE_WHEAT", 0, 3)\
    .tile("TILE_PUDDLE_1", 1, 0)\
    .tile("TILE_PUDDLE_2", 0, 1)\
    .tile("TILE_PUDDLE_3", 1, 1)\
    .tile("TILE_PUDDLE_4", 2, 0)

ITEMS_TILEMAP = TileMapDefinition(1, 1, 1, 1, 30, 30)\
    .tile("potato", 0, 0)
