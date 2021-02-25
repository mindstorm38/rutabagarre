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


# ADD THE FOLLOWINGS IF NEEDED
"""
.tile("TILE_DIRT_1", 2, 0)\
.tile("TILE_DIRT_2", 3, 0)\
.tile("TILE_DIRT_3", 4, 0)\
.tile("TILE_DIRT_4", 2, 1)\
.tile("TILE_DIRT_6", 4, 1)\
.tile("TILE_DIRT_7", 2, 2)\
.tile("TILE_DIRT_8", 3, 2)\
.tile("TILE_DIRT_9", 4, 2)\
.tile("TILE_GRASS_HOLED_3", 7, 0)\
.tile("TILE_GRASS_HOLED_4", 5, 1)\
.tile("TILE_GRASS_HOLED_6", 7, 1)\
.tile("TILE_GRASS_HOLED_7", 5, 2)\
.tile("TILE_GRASS_HOLED_8", 6, 2)\
.tile("TILE_GRASS_HOLED_9", 7, 2)\
.tile("TILE_GRASS_1", 8, 0)\
.tile("TILE_GRASS_4", 8, 1)\
.tile("TILE_GRASS_6", 10, 1)\
.tile("TILE_GRASS_7", 8, 2)\
.tile("TILE_GRASS_8", 9, 2)\
.tile("TILE_GRASS_9", 10, 2)\
.tile("TILE_FARMLAND", 0, 0)\
.tile("TILE_PUDDLE_1", 1, 0)\
.tile("TILE_PUDDLE_2", 0, 1)\
.tile("TILE_PUDDLE_3", 1, 1)\
.tile("TILE_PUDDLE_4", 2, 0)\
.tile("TILE_STONE_1", 2, 3)\
.tile("TILE_STONE_2", 3, 3)\
.tile("TILE_STONE_3", 4, 3)\
.tile("TILE_STONE_4", 2, 4)\
.tile("TILE_STONE_6", 4, 4)\
.tile("TILE_DIRT_STONE_4", 8, 7)\
.tile("TILE_DIRT_STONE_6", 10, 7)\
.tile("TILE_DIRT_STONE_7", 8, 8)\
.tile("TILE_DIRT_STONE_8", 9, 8)\
.tile("TILE_DIRT_STONE_9", 10, 8)\
.tile("TILE_GRASS_DIRT_STONE_4", 8, 4)\
.tile("TILE_GRASS_DIRT_STONE_6", 10, 4)\
.tile("TILE_GRASS_DIRT_STONE_7", 8, 5)\
.tile("TILE_GRASS_DIRT_STONE_8", 9, 5)\
.tile("TILE_GRASS_DIRT_STONE_9", 10, 5)
"""
TERRAIN_TILEMAP = TileMapDefinition(0, 0, 1, 1, 16, 16)\
    .tile("TILE_DIRT_5", 3, 1)\
    .tile("TILE_GRASS_HOLED_1", 5, 0)\
    .tile("TILE_GRASS_HOLED_2", 6, 0)\
    .tile("TILE_GRASS_2", 9, 0)\
    .tile("TILE_GRASS_3", 10, 0)\
    .tile("TILE_GRASS_5", 9, 1)\
    .tile("TILE_WHEAT", 0, 3)\
    .tile("TILE_STONE_5", 3, 4)\
    .tile("TILE_STONE_7", 2, 5)\
    .tile("TILE_STONE_8", 3, 5)\
    .tile("TILE_STONE_9", 4, 5)\
    .tile("TILE_STONE_10", 2, 6)\
    .tile("TILE_STONE_11", 3, 6)\
    .tile("TILE_DIRT_STONE_1", 8, 6)\
    .tile("TILE_DIRT_STONE_2", 9, 6)\
    .tile("TILE_DIRT_STONE_3", 10, 6)\
    .tile("TILE_DIRT_STONE_10", 11, 6)\
    .tile("TILE_DIRT_STONE_11", 12, 6)\
    .tile("TILE_DIRT_STONE_12", 11, 7)\
    .tile("TILE_DIRT_STONE_13", 12, 7)\
    .tile("TILE_DIRT_STONE_14", 11, 8)\
    .tile("TILE_GRASS_DIRT_STONE_1", 8, 3)\
    .tile("TILE_GRASS_DIRT_STONE_2", 9, 3)\
    .tile("TILE_GRASS_DIRT_STONE_3", 10, 3)

ITEMS_TILEMAP = TileMapDefinition(1, 1, 1, 1, 30, 30)\
    .tile("potato", 0, 0)\
    .tile("corn", 1, 0)\
    .tile("carrot", 2, 0)
