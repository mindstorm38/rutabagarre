from typing import List, Union, Tuple, Generator, Dict, TypeVar, Callable, Any, Optional

from entity.player import Player, PlayerColor, IncarnationType
from entity.effect import Effect, EffectType
from entity.hitbox import Hitbox
from entity.floor import Floor
from entity.item import Item
from entity import Entity


E = TypeVar("E", bound=Entity)
AddEntityCallback = Optional[Callable[[Entity], None]]
RemoveEntityCallback = Optional[Callable[[int], None]]


class Tile:

    TILE_AIR = ord(" ")

    TILE_DIRT_1 = ord("A")
    TILE_DIRT_2 = ord("B")
    TILE_DIRT_3 = ord("C")
    TILE_DIRT_4 = ord("D")
    TILE_DIRT_5 = ord("E")
    TILE_DIRT_6 = ord("F")
    TILE_DIRT_7 = ord("G")
    TILE_DIRT_8 = ord("H")
    TILE_DIRT_9 = ord("I")

    TILE_GRASS_LIGHT_1 = ord("J")
    TILE_GRASS_LIGHT_2 = ord("K")
    TILE_GRASS_LIGHT_3 = ord("L")
    TILE_GRASS_LIGHT_4 = ord("M")
    TILE_GRASS_LIGHT_6 = ord("N")
    TILE_GRASS_LIGHT_7 = ord("O")
    TILE_GRASS_LIGHT_8 = ord("P")
    TILE_GRASS_LIGHT_9 = ord("Q")

    TILE_GRASS_DARK_1 = ord("R")
    TILE_GRASS_DARK_2 = ord("S")
    TILE_GRASS_DARK_3 = ord("T")
    TILE_GRASS_DARK_4 = ord("U")
    TILE_GRASS_DARK_6 = ord("V")
    TILE_GRASS_DARK_7 = ord("W")
    TILE_GRASS_DARK_8 = ord("X")
    TILE_GRASS_DARK_9 = ord("Y")

    TILE_FARMLAND = ord("Z")

    TILE_WHEAT = ord("a")

    TILE_PUDDLE_1 = ord("b")
    TILE_PUDDLE_2 = ord("c")
    TILE_PUDDLE_3 = ord("d")
    TILE_PUDDLE_4 = ord("e")

    VALID_TILES_IDS = {
        TILE_DIRT_1,
        TILE_DIRT_2,
        TILE_DIRT_3,
        TILE_DIRT_4,
        TILE_DIRT_5,
        TILE_DIRT_6,
        TILE_DIRT_7,
        TILE_DIRT_8,
        TILE_DIRT_9,

        TILE_GRASS_LIGHT_1,
        TILE_GRASS_LIGHT_2,
        TILE_GRASS_LIGHT_3,
        TILE_GRASS_LIGHT_4,
        TILE_GRASS_LIGHT_6,
        TILE_GRASS_LIGHT_7,
        TILE_GRASS_LIGHT_8,
        TILE_GRASS_LIGHT_9,

        TILE_GRASS_DARK_1,
        TILE_GRASS_DARK_2,
        TILE_GRASS_DARK_3,
        TILE_GRASS_DARK_4,
        TILE_GRASS_DARK_6,
        TILE_GRASS_DARK_7,
        TILE_GRASS_DARK_8,
        TILE_GRASS_DARK_9,

        TILE_FARMLAND,

        TILE_WHEAT,

        TILE_PUDDLE_1,
        TILE_PUDDLE_2,
        TILE_PUDDLE_3,
        TILE_PUDDLE_4
    }

    VALID_TILES = {chr(i) for i in VALID_TILES_IDS}


class Stage:

    __slots__ = "entities", "_size", "_terrain", "_spawn_points", "_players", \
                "_add_entity_cb", "_remove_entity_cb"

    def __init__(self, width: int, height: int):

        self.entities: List[Entity] = []

        self._size = (width, height)
        self._terrain = bytearray(width * height)

        self._spawn_points: List[List[int, int, bool]] = []
        self._players: Dict[int, Tuple[Player, int]] = {}

        self._add_entity_cb: AddEntityCallback = None
        self._remove_entity_cb: RemoveEntityCallback = None

    def update(self):
        i = 0
        while i < len(self.entities):
            entity = self.entities[i]
            if entity.is_dead():
                euid = self.entities.pop(i).get_uid()
                if self._remove_entity_cb is not None:
                    self._remove_entity_cb(euid)
            else:
                entity.update()
                i += 1

    def add_entity(self, constructor: Callable[['Stage', Any], E], *args, **kwargs) -> E:
        entity = constructor(self, *args, **kwargs)
        self.entities.append(entity)
        if self._add_entity_cb is not None:
            self._add_entity_cb(entity)
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

    def add_effect(self, effect_type: EffectType, duration: float, x: float, y: float):
        self.add_entity(Effect, effect_type, duration).set_position(x, y)

    def get_entities(self) -> List[Entity]:
        return self.entities

    def foreach_colliding_entity(self, box: Hitbox, *, predicate: Optional[Callable[[Entity], bool]] = None) -> Generator[Entity, None, None]:
        for entity in self.entities:
            if predicate is None or predicate(entity):
                if entity.get_hitbox().intersects(box):
                    yield entity

    def get_player(self, player_idx: int) -> Optional[Player]:
        data = self._players.get(player_idx)
        return None if data is None else data[0]

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

    def add_spawn_point(self, x: float, y: float) -> None:
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

    def for_each_tile(self) -> Generator[Tuple[int, int, int], None, None]:
        i = 0
        for y in range(self._size[1]):
            for x in range(self._size[0]):
                yield x, y, self._terrain[i]
                i += 1

    # Callbacks

    def set_add_entity_callback(self, callback: AddEntityCallback):
        self._add_entity_cb = callback

    def set_remove_entity_callback(self, callback: RemoveEntityCallback):
        self._remove_entity_cb = callback

    # Factory

    @classmethod
    def new_example_stage(cls) -> 'Stage':

        stage = cls(50, 15)

        stage.set_terrain(
            15, 2,
            b"JKKKKKKKKKKKKKKKKKKKKL",
            b"EEEEEEEEEEEEEEEEEEEEEE",
            b" EEEEEEEEEEEEEEEEEEEE"
        )
        floor = stage.add_entity(Floor)
        floor.get_hitbox().set_positions(15, 2, 37, 4)

        stage.set_terrain(
            18, 8,
            b"JKKL",
        )
        floor = stage.add_entity(Floor)
        floor.get_hitbox().set_positions(18, 7, 22, 8)

        stage.set_terrain(
            24, 12,
            b"JKKL",
        )
        floor = stage.add_entity(Floor)
        floor.get_hitbox().set_positions(24, 11, 28, 12)

        stage.set_terrain(
            30, 8,
            b"JKKL",
        )
        floor = stage.add_entity(Floor)
        floor.get_hitbox().set_positions(30, 7, 34, 8)

        stage.add_spawn_point(23, 5)
        stage.add_spawn_point(29, 5)
        stage.add_spawn_point(17, 5)
        stage.add_spawn_point(35, 5)

        stage.add_entity(Item, IncarnationType.POTATO).set_position(26, 5)
        stage.add_entity(Item, IncarnationType.POTATO).set_position(20, 9)
        stage.add_entity(Item, IncarnationType.POTATO).set_position(32, 9)

        return stage
