from builtins import reversed
from typing import List, Union, Tuple, Iterable
from entity import Entity


class Tile:

    TILE_AIR = ord(" ")
    TILE_DIRT = ord("D")
    TILE_GRASS = ord("G")
    TILE_FARMLAND = ord("F")
    TILE_WHEAT = ord("W")
    TILE_PUDDLE = ord("P")

    VALID_TILES_IDS = {
        TILE_AIR,
        TILE_DIRT,
        TILE_GRASS,
        TILE_FARMLAND,
        TILE_WHEAT,
        TILE_PUDDLE
    }

    VALID_TILES = {chr(i) for i in VALID_TILES_IDS}


class Stage:

    __slots__ = "entities", "_size", "_terrain"

    def __init__(self, width: int, height: int):
        self.entities: List[Entity] = []

        self._size = (width, height)
        self._terrain = bytearray(width * height)

    def update(self):
        for entity in self.entities:
            entity.update()

    def set_terrain(self, left: int, bottom: int, *terrain: Union[bytes, bytearray]):
        for row in reversed(terrain):
            if left + len(row) >= self._size[0]:
                raise ValueError("Row too long.")
            index = self.get_tile_index(left, bottom)
            self._terrain[index:index + len(row)] = row
            bottom += 1

    def get_terrain(self) -> bytearray:
        return self._terrain

    def get_tile_index(self, x: int, y: int) -> int:
        return x + y * self._size[0]

    def get_index_tile(self, index: int) -> Tuple[int, int]:
        return index % self._size[0], index // self._size[0]

    def get_size(self) -> Tuple[int, int]:
        return self._size

    def get_tile(self, x: int, y: int) -> str:
        width, height = self._size
        if 0 <= x < width and 0 <= y < height:
            return chr(self._terrain[self.get_tile_index(x, y)])
        else:
            return " "

    def set_tile(self, x: int, y: int, tile: str):
        width, height = self._size
        if 0 <= x < width and 0 <= y < height:
            self._terrain[self.get_tile_index(x, y)] = ord(tile)

    def for_each_tile(self) -> Iterable[Tuple[int, int, int]]:
        i = 0
        for y in range(self._size[1]):
            for x in range(self._size[0]):
                yield x, y, self._terrain[i]
                i += 1

    @classmethod
    def new_example_stage(cls) -> 'Stage':

        stage = cls(30, 10)

        stage.set_terrain(6, 7,
            b"GGGGGGGGGGGGGGGGGG",
            b"DDDDDDDDDDDDDDDDDD",
            b" DDDDDDDDDDDDDDDD "
        )

        return stage
