from typing import List, Union, Tuple, Iterable, Dict, TypeVar, Callable, Any, Optional

from entity.player import Player, PlayerColor
from entity.hitbox import Hitbox
from entity import Entity
from entity.hitbox import Hitbox


E = TypeVar("E", bound=Entity)
NewEntityCallback = Optional[Callable[[Entity], None]]


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

    __slots__ = "entities", "_size", "_terrain", "_spawn_points", "_players", \
                "_new_entity_cb"

    def __init__(self, width: int, height: int):

        self.entities: List[Entity] = []

        self._size = (width, height)
        self._terrain = bytearray(width * height)

        self._spawn_points: List[List[int, int, bool]] = []
        self._players: Dict[int, Tuple[Player, int]] = {}

        self._new_entity_cb: NewEntityCallback = None

    def update(self):
        for entity in self.entities:
            entity.update()

    def add_entity(self, constructor: Callable[['Stage', Any], E], *args, **kwargs) -> E:
        entity = constructor(self, *args, **kwargs)
        self.entities.append(entity)
        if self._new_entity_cb is not None:
            self._new_entity_cb(entity)
        return entity

    def add_player(self, player_idx: int, color: PlayerColor):

        try:
            index, x, y = next((i, x, y) for i, (x, y, used) in enumerate(self._spawn_points) if not used)
        except StopIteration:
            raise ValueError("No more player spawn point available in this world.")

        self._spawn_points[index][2] = True
        player = self.add_entity(Player, player_idx, color)
        player.set_position(x, y)
        self._players[player_idx] = (player, index)

    def get_entities(self) -> List[Entity]:
        return self.entities

    def foreach_colliding_entities(self, box: Hitbox, *, only_hard: bool = False) -> Iterable[Entity]:
        for entity in self.entities:
            if not only_hard or entity.get_hard_hitbox():
                # TODO
                pass

    # Terrain

    def set_terrain(self, left: int, bottom: int, *terrain: Union[bytes, bytearray]):
        for row in reversed(terrain):
            if left + len(row) >= self._size[0]:
                raise ValueError("Row too long.")
            index = self.get_tile_index(left, bottom)
            self._terrain[index:index + len(row)] = row
            bottom += 1

    def get_terrain(self) -> bytearray:
        return self._terrain

    def add_spawn_point(self, x: int, y: int):
        self._spawn_points.append([x, y, False])

    # Tiles

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

    # Callbacks

    def set_new_entity_callback(self, callback: NewEntityCallback):
        self._new_entity_cb = callback

    @classmethod
    def new_example_stage(cls) -> 'Stage':

        stage = cls(30, 10)

        stage.set_terrain(6, 2,
            b"GGGGGGGGGGGGGGGGGG",
            b"DDDDDDDDDDDDDDDDDD",
            b" DDDDDDDDDDDDDDDD "
        )

        stage.add_spawn_point(7, 5)
        stage.add_spawn_point(23, 5)

        return stage

    # Other methods

    def get_hit_entities(self, hitbox: Hitbox, vect: Tuple[float, float]) -> List[Entity]:
        """
        Returns the list of entities hit by the hitbox if it is moved
        :param hitbox: hitbox to move
        :param vect: directional vector of the hitbox, [x, y]
        :return: list of hit entities
        """
        return Stage.get_hit_entities_in_list(hitbox, vect, self.entities)

    @staticmethod
    def get_hit_entities_in_list(hitbox: Hitbox, vect: Tuple[float, float], entities: List[Entity]) -> List[Entity]:
        """
        Returns the list of entities hit by the hitbox if it is moved
        :param hitbox: hitbox to move
        :param vect: directional vector of the hitbox, [x, y]
        :param entities: list of entities to search on
        :return: list of hit entities
        """
        hitbox_copy = hitbox.copy()
        hitbox_copy.expand(vect[0], vect[1])
        hit_entities = []

        if vect[0] != 0:  # there is a movement on the x-axis
            for entity in entities:
                if entity.get_hard_hitbox() and hitbox_copy.intersects_x(entity.get_hitbox()):
                    hit_entities.append(entity)

        if vect[1] != 0:  # there is a movement on the y-axis
            for entity in entities:
                if (
                        entity.get_hard_hitbox and
                        hitbox_copy.intersects_y(entity.get_hitbox()) and
                        entity not in hit_entities
                ):
                    hit_entities.append(entity)

        return hit_entities
