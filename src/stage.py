from typing import List, Union, Tuple, Generator, Dict, TypeVar, Callable, Any, Optional
import random
import time

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
    # Unused tiles are commented
    # TILE_DIRT_1 = ord("A")
    # TILE_DIRT_2 = ord("B")
    # TILE_DIRT_3 = ord("C")
    # TILE_DIRT_4 = ord("D")
    TILE_DIRT_5 = ord("E")
    # TILE_DIRT_6 = ord("F")
    # TILE_DIRT_7 = ord("G")
    # TILE_DIRT_8 = ord("H")
    # TILE_DIRT_9 = ord("I")

    TILE_GRASS_HOLED_1 = ord("J")
    TILE_GRASS_HOLED_2 = ord("K")
    # TILE_GRASS_HOLED_3 = ord("L")
    # TILE_GRASS_HOLED_4 = ord("M")
    # TILE_GRASS_HOLED_6 = ord("N")
    # TILE_GRASS_HOLED_7 = ord("O")
    # TILE_GRASS_HOLED_8 = ord("P")
    # TILE_GRASS_HOLED_9 = ord("Q")

    # TILE_GRASS_1 = ord("R")
    TILE_GRASS_2 = ord("S")
    TILE_GRASS_3 = ord("T")
    # TILE_GRASS_4 = ord("U")
    TILE_GRASS_5 = ord("V")
    # TILE_GRASS_6 = ord("W")
    # TILE_GRASS_7 = ord("X")
    # TILE_GRASS_8 = ord("Y")
    # TILE_GRASS_9 = ord("Z")

    # TILE_FARMLAND = ord("a")

    TILE_WHEAT = ord("b")

    # TILE_PUDDLE_1 = ord("c")
    # TILE_PUDDLE_2 = ord("d")
    # TILE_PUDDLE_3 = ord("e")
    # TILE_PUDDLE_4 = ord("f")

    # TILE_STONE_1 = ord("g")
    # TILE_STONE_2 = ord("h")
    # TILE_STONE_3 = ord("i")
    # TILE_STONE_4 = ord("j")
    TILE_STONE_5 = ord("k")
    # TILE_STONE_6 = ord("l")
    TILE_STONE_7 = ord("m")
    TILE_STONE_8 = ord("n")
    TILE_STONE_9 = ord("o")
    TILE_STONE_10 = ord("8")
    TILE_STONE_11 = ord("9")

    TILE_DIRT_STONE_1 = ord("p")
    TILE_DIRT_STONE_2 = ord("q")
    TILE_DIRT_STONE_3 = ord("r")
    # TILE_DIRT_STONE_4 = ord("s")
    # TILE_DIRT_STONE_5 = ord("t")
    # TILE_DIRT_STONE_6 = ord("u")
    # TILE_DIRT_STONE_7 = ord("v")
    # TILE_DIRT_STONE_8 = ord("w")
    # TILE_DIRT_STONE_9 = ord("x")
    TILE_DIRT_STONE_10 = ord("0")
    TILE_DIRT_STONE_11 = ord("&")
    TILE_DIRT_STONE_12 = ord("~")
    TILE_DIRT_STONE_13 = ord("#")
    TILE_DIRT_STONE_14 = ord("{")

    TILE_GRASS_DIRT_STONE_1 = ord("y")
    TILE_GRASS_DIRT_STONE_2 = ord("z")
    TILE_GRASS_DIRT_STONE_3 = ord("1")
    # TILE_GRASS_DIRT_STONE_4 = ord("2")
    # TILE_GRASS_DIRT_STONE_5 = ord("3")
    # TILE_GRASS_DIRT_STONE_6 = ord("4")
    # TILE_GRASS_DIRT_STONE_7 = ord("5")
    # TILE_GRASS_DIRT_STONE_8 = ord("6")
    # TILE_GRASS_DIRT_STONE_9 = ord("7")

    VALID_TILES_IDS = {
        # TILE_DIRT_1,
        # TILE_DIRT_2,
        # TILE_DIRT_3,
        # TILE_DIRT_4,
        TILE_DIRT_5,
        # TILE_DIRT_6,
        # TILE_DIRT_7,
        # TILE_DIRT_8,
        # TILE_DIRT_9,

        TILE_GRASS_HOLED_1,
        TILE_GRASS_HOLED_2,
        # TILE_GRASS_HOLED_3,
        # TILE_GRASS_HOLED_4,
        # TILE_GRASS_HOLED_6,
        # TILE_GRASS_HOLED_7,
        # TILE_GRASS_HOLED_8,
        # TILE_GRASS_HOLED_9,

        # TILE_GRASS_1,
        TILE_GRASS_2,
        TILE_GRASS_3,
        # TILE_GRASS_4,
        TILE_GRASS_5,
        # TILE_GRASS_6,
        # TILE_GRASS_7,
        # TILE_GRASS_8,
        # TILE_GRASS_9,

        # TILE_FARMLAND,

        TILE_WHEAT,

        # TILE_PUDDLE_1,
        # TILE_PUDDLE_2,
        # TILE_PUDDLE_3,
        # TILE_PUDDLE_4,

        # TILE_STONE_1,
        # TILE_STONE_2,
        # TILE_STONE_3,
        # TILE_STONE_4,
        TILE_STONE_5,
        # TILE_STONE_6,
        TILE_STONE_7,
        TILE_STONE_8,
        TILE_STONE_9,
        TILE_STONE_10,
        TILE_STONE_11,

        TILE_DIRT_STONE_1,
        TILE_DIRT_STONE_2,
        TILE_DIRT_STONE_3,
        # TILE_DIRT_STONE_4,
        # TILE_DIRT_STONE_5,
        # TILE_DIRT_STONE_6,
        # TILE_DIRT_STONE_7,
        # TILE_DIRT_STONE_8,
        # TILE_DIRT_STONE_9,
        TILE_DIRT_STONE_10,
        TILE_DIRT_STONE_11,
        TILE_DIRT_STONE_12,
        TILE_DIRT_STONE_13,
        TILE_DIRT_STONE_14,

        TILE_GRASS_DIRT_STONE_1,
        TILE_GRASS_DIRT_STONE_2,
        TILE_GRASS_DIRT_STONE_3
        # TILE_GRASS_DIRT_STONE_4,
        # TILE_GRASS_DIRT_STONE_5,
        # TILE_GRASS_DIRT_STONE_6,
        # TILE_GRASS_DIRT_STONE_7,
        # TILE_GRASS_DIRT_STONE_8,
        # TILE_GRASS_DIRT_STONE_9

    }

    VALID_TILES = {chr(i) for i in VALID_TILES_IDS}


class Stage:

    __slots__ = "_entities", "_size", "_terrain", \
                "_running", "_finished", "_winner", \
                "_spawn_points", "_players", "_living_players_count", \
                "_items_count", "_next_item_spawn", \
                "_add_entity_cb", "_remove_entity_cb"

    def __init__(self, width: int, height: int):

        self._entities: List[Entity] = []

        self._size = (width, height)
        self._terrain = bytearray(width * height)

        self._running = True
        self._finished = False
        self._winner: Optional[Player] = None

        self._spawn_points: List[List[int, int, bool]] = []
        self._players: Dict[int, Tuple[Player, int]] = {}
        self._living_players_count: int = 0

        self._items_count: int = 0
        self._next_item_spawn: float = 0

        self._add_entity_cb: AddEntityCallback = None
        self._remove_entity_cb: RemoveEntityCallback = None

    def update(self):

        if self._running:

            i = 0
            while i < len(self._entities):

                entity = self._entities[i]

                if entity.is_dead():

                    euid = self._entities.pop(i).get_uid()

                    if isinstance(entity, Player):

                        player_data = self._players.get(entity.get_player_index())
                        if player_data is not None:
                            self._spawn_points[player_data[1]][2] = False
                            self._living_players_count -= 1
                            if self._living_players_count == 1:
                                # S'il ne reste qu'un joueur après en avoir tué un, l'autre gagne.
                                self._finished = True
                                for player, _ in self._players.values():
                                    if not player.is_dead():
                                        self._winner = player

                    elif isinstance(entity, Item):
                        self._items_count -= 1

                    if self._remove_entity_cb is not None:
                        self._remove_entity_cb(euid)

                else:
                    
                    entity.update()
                    i += 1

            if self._next_item_spawn == 0 or time.monotonic() >= self._next_item_spawn:
                self._try_spawn_random_item()

    def add_entity(self, constructor: Callable[['Stage', Any], E], *args, **kwargs) -> E:
        entity = constructor(self, *args, **kwargs)
        self._entities.append(entity)
        if isinstance(entity, Item):
            self._items_count += 1
        if self._add_entity_cb is not None:
            self._add_entity_cb(entity)
        return entity

    def add_player(self, player_idx: int, color: PlayerColor):

        if player_idx in self._players:
            raise ValueError("A player with this index already exists in the stage.")

        try:
            index, x, y = next((i, x, y) for i, (x, y, used) in enumerate(self._spawn_points) if not used)
        except StopIteration:
            raise ValueError("No more player spawn point available in this world.")

        self._spawn_points[index][2] = True
        player = self.add_entity(Player, player_idx, color)
        player.set_position(x, y)
        self._living_players_count += 1
        self._players[player_idx] = (player, index)

    def add_effect(self, effect_type: EffectType, duration: float, x: float, y: float):
        self.add_entity(Effect, effect_type, duration).set_position(x, y)

    def _try_spawn_random_item(self):
        floors = [entity for entity in self._entities if isinstance(entity, Floor)]
        floors_count = len(floors)
        items_limit = floors_count * self._living_players_count
        if floors_count and self._items_count < items_limit:
            floor = random.choice(floors)
            hitbox = floor.get_hitbox()
            x_pos = random.uniform(hitbox.get_min_x(), hitbox.get_max_x())
            y_pos = hitbox.get_max_y() + 1.0
            incarnation_type = random.choice(list(IncarnationType))
            self.add_entity(Item, incarnation_type).set_position(x_pos, y_pos)
            if self._items_count < self._living_players_count:
                next_in = 1
            else:
                next_in = 8
        else:
            next_in = 5
        self._next_item_spawn = time.monotonic() + random.uniform(next_in, next_in + 3.0)

    def get_entities(self) -> List[Entity]:
        return self._entities

    def foreach_colliding_entity(self, box: Hitbox, *, predicate: Optional[Callable[[Entity], bool]] = None) -> Generator[Entity, None, None]:
        for entity in self._entities:
            if predicate is None or predicate(entity):
                if entity.get_hitbox().intersects(box):
                    yield entity

    def get_player(self, player_idx: int) -> Optional[Player]:
        data = self._players.get(player_idx)
        return None if data is None else data[0]

    def get_players(self) -> Dict[int, Player]:
        return {idx: player for idx, (player, _) in self._players.items()}

    def stop_running(self):
        self._running = False

    def is_finished(self) -> bool:
        return self._finished

    def get_winner(self) -> Optional[Player]:
        return self._winner

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

        stage = cls(30, 13)

        stage.set_terrain(
            4, 0,
            b" b    b         b  b",
            b"JSSKSKSKKSKKKKSKSKKSKT",
            b"0q#~qq#{{{~#~qqqqq#~q&",
            b" mnnnkkkkkknknnnkkkno",
            b"     mnkkko 8   mno",
            b"       mno  9"
        )
        floor = stage.add_entity(Floor)
        floor.get_hitbox().set_positions(4, 2, 26, 4)

        stage.set_terrain(
            7, 8,
            b"b",
            b"yzzz",
        )
        floor = stage.add_entity(Floor)
        floor.get_hitbox().set_positions(7, 7, 11, 8)

        stage.set_terrain(
            13, 12,
            b"yzz1",
        )
        floor = stage.add_entity(Floor)
        floor.get_hitbox().set_positions(13, 11, 17, 12)

        stage.set_terrain(
            19, 8,
            b"  b",
            b"yzz1",
        )
        floor = stage.add_entity(Floor)
        floor.get_hitbox().set_positions(19, 7, 23, 8)

        stage.add_spawn_point(12, 5)
        stage.add_spawn_point(18, 5)
        stage.add_spawn_point(6, 5)
        stage.add_spawn_point(24, 5)

        return stage
