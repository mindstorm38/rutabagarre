from view.anim import AnimSurfaceColored, AnimSurface, NewAnimTracker, FARMER_ANIMATION, POTATO_ANIMATION, \
    EFFECTS_ANIMATION, CORN_ANIMATION, CARROT_ANIMATION
from view.tilemap import TileMap, TERRAIN_TILEMAP, ITEMS_TILEMAP
from view.player import get_player_color
from view.controls import KEYS_PLAYERS
from stage import Stage, Tile
from view import View

from entity.player import Player, IncarnationType
from entity.effect import Effect, EffectType
from entity.bullet import Bullet
from entity.item import Item
from entity import Entity

from typing import Optional, Dict, Type, Callable, Tuple, cast
from pygame.event import Event
from pygame import Surface
import traceback
import random
import pygame
import math
import time


class EntityDrawer:

    __slots__ = "entity", "view", "offsets"

    DEBUG_HITBOXES = False

    def __init__(self, entity: Entity, view: 'InGameView', size: Tuple[int, int]):
        self.entity = entity
        self.view = view
        self.offsets = self._calc_offsets(size)

    @classmethod
    def undefined_drawer(cls, entity: Entity, view: 'InGameView'):
        return cls(entity, view, (0, 0))

    def _calc_offsets(self, size: Tuple[int, int]) -> Tuple[int, int]:
        return -int(size[0] / 2), -size[1]

    def _get_draw_pos(self) -> Tuple[int, int]:
        x, y = self.view.get_screen_pos(self.entity.get_x(), self.entity.get_y())
        return x + self.offsets[0], y + self.offsets[1]

    def get_debug_rect(self) -> Tuple[int, int, int, int]:
        hitbox = self.entity.get_hitbox()
        min_x, min_y = self.view.get_screen_pos(hitbox.get_min_x(), hitbox.get_min_y())
        max_x, max_y = self.view.get_screen_pos(hitbox.get_max_x(), hitbox.get_max_y())
        return min_x, max_y, max_x - min_x, min_y - max_y

    def get_camera_x(self) -> Optional[float]:
        return None

    def draw(self, surface: Surface): ...

    def __str__(self):
        return "{}<euid: {}>".format(type(self), self.entity.get_uid())


class PlayerDrawer(EntityDrawer):

    __slots__ = "color", "tracker", "phase_shift", "camera_x", "state"

    BAR_WIDTH, BAR_HEIGHT = 100, 10
    BAR_OFFSET = 40
    BAR_SLEEPING_OFFSET = 25
    HALF_BAR_WIDTH = BAR_WIDTH // 2
    HEALTH_BACKG_COLOR = 16, 26, 11
    MAX_HEALTH_COLOR = 74, 201, 20
    MIN_HEALTH_COLOR = 201, 20, 20
    INCARNATION_COLOR = 47, 82, 212
    INCARNATION_BACK_COLOR = 23, 34, 74

    CAMERA_SPEED = 0.1

    STATE_UNINIT = 0
    STATE_IDLE = 1
    STATE_RUNNING = 2
    STATE_MUTATING = 3
    STATE_ROLLING = 4
    STATE_MISC_ANIM = 5
    STATE_SLEEPING = 6
    STATE_SHOOTING = 7
    STATE_SPECIAL = 8

    NO_COLOR = 255, 255, 255

    MISC_ANIMATIONS = {
        "farmer:rake_attack": (("attack_side", 40, 1),),
        "farmer:spinning_attack": (("attack_down", 40, 2),),
        "potato:punch": (("attack_side", 20, 1),),
        "corn:shot": (("attack_side", 20, 1),),
        "carrot:strike": (("attack_side", 20, 1),),
        "hit": (("hit", 20, 1),),
        "grabing": (("grab", 20, 1),),
        "player:mutation": (("pick", 10, 1),)
    }

    MISC_SOUNDS = {
        "farmer:rake_attack": "sounds/farmerpunch.ogg",
        "farmer:spinning_attack": "sounds/farmerspin.ogg",
        "hit": "sounds/hit.ogg",
        "potato:punch": "sounds/potatopunch.ogg",
        "potato:roll": "sounds/potatoroll.ogg",
        "corn:shot": "sounds/cornshot.ogg",
        "corn:gatling": "sounds/corngatling.ogg",
        "carrot:strike": "sounds/carrotstrike.ogg",
        "carrot:thrust": "sounds/carrotthrust.ogg"
    }

    def __init__(self, entity: Player, view: 'InGameView'):
        super().__init__(entity, view, (InGameView.PLAYER_SIZE, InGameView.PLAYER_SIZE))
        self.color = get_player_color(entity.get_color())
        self.tracker = NewAnimTracker()
        self.phase_shift = random.random() * math.pi
        self.camera_x = entity.get_x()
        self.state = self.STATE_UNINIT

    def get_camera_x(self) -> Optional[float]:
        return self.camera_x

    def draw(self, surface: Surface):

        player = cast(Player, self.entity)
        self.tracker.set_all_reversed(player.get_turned_to_left())

        can_run = player.get_vel_x() != 0 and player.is_on_ground()
        incarnation_type = player.get_incarnation_type()
        is_potato = incarnation_type == IncarnationType.POTATO
        is_corn = incarnation_type == IncarnationType.CORN
        is_carrot = incarnation_type == IncarnationType.CARROT

        for animation in player.foreach_animation():

            if self.state in (self.STATE_IDLE, self.STATE_RUNNING) and animation in self.MISC_ANIMATIONS:
                self.tracker.set_anim(*self.MISC_ANIMATIONS[animation])
                self.state = self.STATE_MISC_ANIM
                if animation == "player:mutation":
                    self.state = self.STATE_MUTATING
            elif animation == "player:unmutation":
                self.state = self.STATE_UNINIT

            if animation in self.MISC_SOUNDS:
                self.view.get_shared_data().play_sound(self.MISC_SOUNDS[animation])

        if self.state in (self.STATE_MUTATING, self.STATE_MISC_ANIM) and self.tracker.get_anim_name() is None:
            self.state = self.STATE_UNINIT
        elif self.state == self.STATE_SPECIAL and not player.is_in_special_action():
            if is_potato:
                self.tracker.set_anim(("attack_roll_end", 14, 1))
            elif is_corn:
                self.tracker.set_anim(("attack_gun_end", 14, 1))
            elif is_carrot:
                self.tracker.set_anim(("attack_sword_end", 14, 1))
            self.state = self.STATE_MISC_ANIM
        elif self.state == self.STATE_SLEEPING and not player.is_sleeping():
            self.tracker.set_anim(("unsleep", 14, 1))
            self.state = self.STATE_MISC_ANIM

        if self.state != self.STATE_SPECIAL and player.is_in_special_action():
            if is_potato:
                self.tracker.set_anim(("attack_roll_start", 14, 1), ("attack_roll_idle", 14, -1))
            elif is_corn:
                self.tracker.set_anim(("attack_gun_start", 14, 1), ("attack_gun_idle", 14, -1))
            elif is_carrot:
                self.tracker.set_anim(("attack_sword_start", 14, 1), ("attack_sword_idle", 14, -1))
            self.state = self.STATE_SPECIAL
        elif self.state != self.STATE_SLEEPING and player.is_sleeping() and incarnation_type is not None:
            self.tracker.set_anim(("sleep", 14, 1), pause_at_end=True)
            self.state = self.STATE_SLEEPING
        elif self.state in (self.STATE_UNINIT, self.STATE_IDLE) and can_run:
            self.tracker.set_anim(("run", 14, -1))
            self.state = self.STATE_RUNNING
        elif self.state in (self.STATE_UNINIT, self.STATE_RUNNING) and not can_run:
            self.tracker.set_anim(("idle", 7, -1))
            self.state = self.STATE_IDLE

        anim_surface = self.view.get_player_anim_surface()
        if self.state != self.STATE_MUTATING:
            if is_potato:
                anim_surface = self.view.get_potato_anim_surface()
            elif is_corn:
                anim_surface = self.view.get_corn_anim_surface()
            elif is_carrot:
                anim_surface = self.view.get_carrot_anim_surface()

        anim_surface.blit_color_on(surface, self._get_draw_pos(), self.tracker, self.color)

        health_ratio = player.get_hp_ratio()
        health_color = _lerp_color(self.MIN_HEALTH_COLOR, self.MAX_HEALTH_COLOR, health_ratio)
        health_bar_x, health_bar_y = self.view.get_screen_pos(self.entity.get_x(), self.entity.get_y())
        if not player.is_sleeping():
            health_bar_y -= InGameView.PLAYER_SIZE + self.BAR_OFFSET
        else:
            health_bar_y += self.BAR_SLEEPING_OFFSET
        health_bar_y -= math.cos(time.monotonic() * 5 + self.phase_shift) * 4

        self._draw_bar(surface, health_bar_x, health_bar_y, health_ratio, health_color, self.HEALTH_BACKG_COLOR)
        if incarnation_type is not None:
            ratio = player.get_incarnation_duration_ratio()
            self._draw_bar(surface, health_bar_x, health_bar_y + self.BAR_HEIGHT, ratio, self.INCARNATION_COLOR, self.INCARNATION_BACK_COLOR)

        self.camera_x += (player.get_x() - self.camera_x) * self.CAMERA_SPEED

    def _draw_bar(self, surface: Surface, x: int, y: int, ratio: float, color: Tuple[int, int, int], back_color: Tuple[int, int, int]):
        x -= self.HALF_BAR_WIDTH
        health_bar_width = int(self.BAR_WIDTH * ratio)
        pygame.draw.rect(surface, back_color, (x + health_bar_width, y, self.BAR_WIDTH - health_bar_width, self.BAR_HEIGHT))
        pygame.draw.rect(surface, color, (x, y, health_bar_width, self.BAR_HEIGHT))


class ItemDrawer(EntityDrawer):

    __slots__ = "tile_surface", "anim_phase_shift"

    ITEMS_NAMES = {
        IncarnationType.POTATO: "potato",
        IncarnationType.CORN: "corn",
        IncarnationType.CARROT: "carrot"
    }

    def __init__(self, entity: Item, view: 'InGameView'):
        super().__init__(entity, view, (InGameView.ITEM_SIZE, InGameView.ITEM_SIZE))
        tile_name = self.ITEMS_NAMES.get(entity.get_incarnation_type())
        self.tile_surface = None if tile_name is None else view.get_item_tilemap().get_tile(tile_name)
        self.anim_phase_shift = random.random() * math.pi

    def draw(self, surface: Surface):
        if self.tile_surface is not None:
            x, y = self._get_draw_pos()
            surface.blit(self.tile_surface, (x, y - max(0.0, math.cos(time.monotonic() * 6 + self.anim_phase_shift) * 4)))


class EffectDrawer(EntityDrawer):

    __slots__ = "anim_surface", "tracker", "effect_type"

    DEBUG_HITBOXES = False

    EFFECT_ANIMS = {
        EffectType.SMOKE: (("smoke", 6, 1),),
        EffectType.SMALL_GROUND_DUST: (("small_ground_dust", 8, 1),),
        EffectType.BIG_GROUND_DUST: (("big_ground_dust", 8, 1),),
        EffectType.SLEEPING: (("sleeping_start", 3, 1), ("sleeping_idle", 3, -1)),
    }

    def __init__(self, entity: Effect, view: 'InGameView'):
        super().__init__(entity, view, (InGameView.EFFECT_SIZE, InGameView.EFFECT_SIZE))
        self.anim_surface = view.get_effect_anim_surface()
        self.tracker = NewAnimTracker()
        self.effect_type = entity.get_effect_type()
        if self.effect_type in self.EFFECT_ANIMS:
            self.tracker.set_anim(*self.EFFECT_ANIMS[self.effect_type])

    def draw(self, surface: Surface):
        self.anim_surface.blit_on(surface, self._get_draw_pos(), self.tracker)


class BulletDrawer(EntityDrawer):

    def __init__(self, entity: Entity, view: 'InGameView'):
        super().__init__(entity, view, (InGameView.EFFECT_SIZE, InGameView.EFFECT_SIZE))
        self.anim_surface = view.get_effect_anim_surface()
        self.tracker = NewAnimTracker()
        self.tracker.set_anim(("corn_bullet", 14, -1))

    def _calc_offsets(self, size: Tuple[int, int]) -> Tuple[int, int]:
        return -int(size[0] / 2), -int(size[1] / 2)

    def draw(self, surface: Surface):
        self.anim_surface.blit_on(surface, self._get_draw_pos(), self.tracker)


class InGameView(View):

    BACKGROUND_COLOR = None

    TILES_NAMES = {
        Tile.TILE_DIRT_1: "TILE_DIRT_1",
        Tile.TILE_DIRT_2: "TILE_DIRT_2",
        Tile.TILE_DIRT_3: "TILE_DIRT_3",
        Tile.TILE_DIRT_4: "TILE_DIRT_4",
        Tile.TILE_DIRT_5: "TILE_DIRT_5",
        Tile.TILE_DIRT_6: "TILE_DIRT_6",
        Tile.TILE_DIRT_7: "TILE_DIRT_7",
        Tile.TILE_DIRT_8: "TILE_DIRT_8",
        Tile.TILE_DIRT_9: "TILE_DIRT_9",

        Tile.TILE_GRASS_HOLED_1: "TILE_GRASS_HOLED_1",
        Tile.TILE_GRASS_HOLED_2: "TILE_GRASS_HOLED_2",
        Tile.TILE_GRASS_HOLED_3: "TILE_GRASS_HOLED_3",
        Tile.TILE_GRASS_HOLED_4: "TILE_GRASS_HOLED_4",
        Tile.TILE_GRASS_HOLED_6: "TILE_GRASS_HOLED_6",
        Tile.TILE_GRASS_HOLED_7: "TILE_GRASS_HOLED_7",
        Tile.TILE_GRASS_HOLED_8: "TILE_GRASS_HOLED_8",
        Tile.TILE_GRASS_HOLED_9: "TILE_GRASS_HOLED_9",

        Tile.TILE_GRASS_1: "TILE_GRASS_1",
        Tile.TILE_GRASS_2: "TILE_GRASS_2",
        Tile.TILE_GRASS_3: "TILE_GRASS_3",
        Tile.TILE_GRASS_4: "TILE_GRASS_4",
        Tile.TILE_GRASS_5: "TILE_GRASS_5",
        Tile.TILE_GRASS_6: "TILE_GRASS_6",
        Tile.TILE_GRASS_7: "TILE_GRASS_7",
        Tile.TILE_GRASS_8: "TILE_GRASS_8",
        Tile.TILE_GRASS_9: "TILE_GRASS_9",

        Tile.TILE_WHEAT: "TILE_WHEAT",

        Tile.TILE_FARMLAND: "TILE_FARMLAND",

        Tile.TILE_PUDDLE_1: "TILE_PUDDLE_1",
        Tile.TILE_PUDDLE_2: "TILE_PUDDLE_2",
        Tile.TILE_PUDDLE_3: "TILE_PUDDLE_3",
        Tile.TILE_PUDDLE_4: "TILE_PUDDLE_4",

        Tile.TILE_STONE_1: "TILE_STONE_1",
        Tile.TILE_STONE_2: "TILE_STONE_2",
        Tile.TILE_STONE_3: "TILE_STONE_3",
        Tile.TILE_STONE_4: "TILE_STONE_4",
        Tile.TILE_STONE_5: "TILE_STONE_5",
        Tile.TILE_STONE_6: "TILE_STONE_6",
        Tile.TILE_STONE_7: "TILE_STONE_7",
        Tile.TILE_STONE_8: "TILE_STONE_8",
        Tile.TILE_STONE_9: "TILE_STONE_9",

        Tile.TILE_DIRT_STONE_1: "TILE_DIRT_STONE_1",
        Tile.TILE_DIRT_STONE_2: "TILE_DIRT_STONE_2",
        Tile.TILE_DIRT_STONE_3: "TILE_DIRT_STONE_3",
        Tile.TILE_DIRT_STONE_4: "TILE_DIRT_STONE_4",
        Tile.TILE_DIRT_STONE_5: "TILE_DIRT_STONE_5",
        Tile.TILE_DIRT_STONE_6: "TILE_DIRT_STONE_6",
        Tile.TILE_DIRT_STONE_7: "TILE_DIRT_STONE_7",
        Tile.TILE_DIRT_STONE_8: "TILE_DIRT_STONE_8",
        Tile.TILE_DIRT_STONE_9: "TILE_DIRT_STONE_9",

        Tile.TILE_GRASS_DIRT_STONE_1: "TILE_GRASS_DIRT_STONE_1",
        Tile.TILE_GRASS_DIRT_STONE_2: "TILE_GRASS_DIRT_STONE_2",
        Tile.TILE_GRASS_DIRT_STONE_3: "TILE_GRASS_DIRT_STONE_3",
        Tile.TILE_GRASS_DIRT_STONE_4: "TILE_GRASS_DIRT_STONE_4",
        Tile.TILE_GRASS_DIRT_STONE_5: "TILE_GRASS_DIRT_STONE_5",
        Tile.TILE_GRASS_DIRT_STONE_6: "TILE_GRASS_DIRT_STONE_6",
        Tile.TILE_GRASS_DIRT_STONE_7: "TILE_GRASS_DIRT_STONE_7",
        Tile.TILE_GRASS_DIRT_STONE_8: "TILE_GRASS_DIRT_STONE_8",
        Tile.TILE_GRASS_DIRT_STONE_9: "TILE_GRASS_DIRT_STONE_9"
    }

    ENTITY_DRAWERS: Dict[Type[Entity], Callable[[Entity, 'InGameView'], EntityDrawer]] = {
        Player: PlayerDrawer,
        Item: ItemDrawer,
        Effect: EffectDrawer,
        Bullet: BulletDrawer
    }

    TILE_SIZE = 48
    PLAYER_SIZE = 96
    ITEM_SIZE = 96
    EFFECT_SIZE = 96

    CAMERA_WIDTH_MIN = 20
    CAMERA_WIDTH_MARGIN = 8

    CAMERA_UPDATE_THRESHOLD = 0.02

    def __init__(self):

        super().__init__()

        self._background_surface: Optional[Surface] = None

        self._terrain_tilemap: Optional[TileMap] = None
        self._item_tilemap: Optional[TileMap] = None
        self._player_anim_surface: Optional[AnimSurfaceColored] = None
        self._potato_anim_surface: Optional[AnimSurfaceColored] = None
        self._corn_anim_surface: Optional[AnimSurfaceColored] = None
        self._carrot_anim_surface: Optional[AnimSurfaceColored] = None
        self._effect_anim_surface: Optional[AnimSurface] = None

        self._stage: Optional[Stage] = None
        self._stage_size = (0, 0)
        self._stage_ratio = 0

        # Surfaces "not-scaled"
        self._terrain_surface: Optional[Surface] = None
        self._final_surface: Optional[Surface] = None
        self._y_offset: int = 0

        self._camera_range = (0, 0, 0)  # (start, width, mid)
        self._camera_dirty_pos = False
        self._camera_last_next_update: float = 0

        self._scaled_surface: Optional[Surface] = None
        self._scaled_surface_pos = (0, 0)

        self._entities: Dict[int, EntityDrawer] = {}

        self._stop_running_at: Optional[float] = None

    def on_enter(self):

        print("Loading stage...")

        self._stop_running_at = None
        self._entities.clear()

        self._background_surface = self._shared_data.get_image("fightbackground.png")

        self._shared_data.play_music("musics/fightmusic.ogg")

        game = self._shared_data.get_game()
        self._stage = game.get_stage()

        if self._stage is None:
            print("=> No stage ready in the game.")
        else:

            self._stage.set_add_entity_callback(self._on_entity_added)
            self._stage.set_remove_entity_callback(self._on_entity_removed)

            for entity in self._stage.get_entities():
                self._on_entity_added(entity)

            self._redraw_terrain()

            print("=> Stage loaded.")

    def on_quit(self):
        if self._stage is not None:
            self._stage.set_add_entity_callback(None)
            self._stage.set_remove_entity_callback(None)
            self._stage = None

    def get_item_tilemap(self) -> TileMap:
        return self._item_tilemap

    def get_player_anim_surface(self) -> Optional[AnimSurfaceColored]:
        return self._player_anim_surface

    def get_potato_anim_surface(self) -> Optional[AnimSurfaceColored]:
        return self._potato_anim_surface

    def get_corn_anim_surface(self) -> Optional[AnimSurfaceColored]:
        return self._corn_anim_surface

    def get_carrot_anim_surface(self) -> Optional[AnimSurfaceColored]:
        return self._carrot_anim_surface

    def get_effect_anim_surface(self) -> Optional[AnimSurface]:
        return self._effect_anim_surface

    def get_screen_pos(self, x: float, y: float) -> Tuple[int, int]:
        return int(x * self.TILE_SIZE), self._y_offset - int(y * self.TILE_SIZE)

    # Private #

    def _redraw_terrain(self):

        print("Drawing stage terrain...")

        width, height = self._stage.get_size()

        height_factor = math.ceil(width / height)
        old_height = height
        height *= height_factor

        unscaled_size = (
            width * self.TILE_SIZE,
            height * self.TILE_SIZE
        )

        self._y_offset = unscaled_size[1] - (((height - old_height) // 2) + 1) * self.TILE_SIZE

        self._terrain_surface = Surface(unscaled_size, pygame.HWSURFACE, self._background_surface)
        self._final_surface = Surface(unscaled_size, pygame.HWSURFACE)

        pygame.transform.scale(self._background_surface, unscaled_size, self._terrain_surface)

        for x, y, tile_id in self._stage.for_each_tile():
            tile_name = self.TILES_NAMES.get(tile_id)
            if tile_name is not None:
                tile_surface = self._terrain_tilemap.get_tile(tile_name)
                if tile_surface is not None:
                    self._terrain_surface.blit(tile_surface, (x * self.TILE_SIZE, self._y_offset - y * self.TILE_SIZE))

        self._stage_size = (width, height)
        self._stage_ratio = height / width

        print("=> Stage terrain drawn!")

    def _recompute_camera_scale(self, surface: Surface):

        if self._camera_dirty_pos:

            range_width = self._camera_range[1]
            range_invert_ratio = self._stage_size[0] / range_width

            start_ratio = self._camera_range[0] / self._stage_size[0]

            surface_width, surface_height = surface.get_size()

            scaled_size = (
                surface_width * range_invert_ratio,
                surface_width * range_invert_ratio * self._stage_ratio
            )

            if self._scaled_surface is None:
                self._scaled_surface = Surface(scaled_size, pygame.HWSURFACE)

            self._scaled_surface_pos = (-scaled_size[0] * start_ratio, (surface_height - scaled_size[1]) / 2)

    def _on_entity_added(self, entity: Entity):
        # print("Entity added to view: {}".format(entity))
        constructor = self.ENTITY_DRAWERS.get(type(entity))
        if constructor is None:
            print("=> This entity has no drawer constructor, using undefined drawer.")
            constructor = EntityDrawer.undefined_drawer
        try:
            drawer = constructor(entity, self)
            self._entities[entity.get_uid()] = drawer
        except (Exception,) as e:
            print("Failed to construct {}: {}".format(constructor, e))
            traceback.print_exc()

    def _on_entity_removed(self, euid: int):
        # print("Entity removed from view: {}".format(euid))
        if euid in self._entities:
            del self._entities[euid]

    def _inner_init(self):

        self._terrain_tilemap = self._shared_data.get_tilemap("terrain.png", TERRAIN_TILEMAP)\
            .copy_scaled(self.TILE_SIZE, self.TILE_SIZE)

        self._item_tilemap = self._shared_data.get_tilemap("items.png", ITEMS_TILEMAP)\
            .copy_scaled(self.ITEM_SIZE, self.ITEM_SIZE)

        self._player_anim_surface = self._shared_data\
            .new_anim_colored("farmer", FARMER_ANIMATION, self.PLAYER_SIZE, self.PLAYER_SIZE)

        self._potato_anim_surface = self._shared_data\
            .new_anim_colored("potato", POTATO_ANIMATION, self.PLAYER_SIZE, self.PLAYER_SIZE)

        self._corn_anim_surface = self._shared_data\
            .new_anim_colored("corn", CORN_ANIMATION, self.PLAYER_SIZE, self.PLAYER_SIZE)

        self._carrot_anim_surface = self._shared_data\
            .new_anim_colored("carrot", CARROT_ANIMATION, self.PLAYER_SIZE, self.PLAYER_SIZE)

        self._effect_anim_surface = AnimSurface(self.EFFECT_SIZE, self.EFFECT_SIZE, [
            self._shared_data.get_anim("effects.png", EFFECTS_ANIMATION)
        ])

    def _inner_pre_draw(self, surface: Surface):

        if self._stage is None:
            surface.fill((0, 0, 0))
            return

        self._final_surface.blit(self._terrain_surface, (0, 0))

        # Camera
        camera_range_min = None
        camera_range_max = None

        for entity_drawer in self._entities.values():
            entity_drawer.draw(self._final_surface)
            if entity_drawer.DEBUG_HITBOXES:
                pygame.draw.rect(self._final_surface, (255, 255, 255, 60), entity_drawer.get_debug_rect(), 2)
            camera_x = entity_drawer.get_camera_x()
            if camera_x is not None:
                if camera_range_min is None:
                    camera_range_min = camera_range_max = camera_x
                elif camera_range_min > camera_x:
                    camera_range_min = camera_x
                elif camera_range_max < camera_x:
                    camera_range_max = camera_x

        if camera_range_min is None:
            camera_range_width = self.CAMERA_WIDTH_MIN
            camera_range_mid = self._stage_size[0]
        else:
            camera_range_width = max(cast(float, self.CAMERA_WIDTH_MIN), min(
                cast(float, self._stage_size[0]),
                camera_range_max - camera_range_min + self.CAMERA_WIDTH_MARGIN
            ))
            camera_range_mid = min(cast(float, self._stage_size[0]), max(
                0.0, (camera_range_min + camera_range_max) / 2
            ))

        if abs(self._camera_range[2] - camera_range_mid) >= self.CAMERA_UPDATE_THRESHOLD:
            if abs(self._camera_range[1] - camera_range_width) >= self.CAMERA_UPDATE_THRESHOLD:
                self._scaled_surface = None
            self._camera_dirty_pos = True
            self._camera_range = (camera_range_mid - (camera_range_width / 2), camera_range_width, camera_range_mid)

        # Recompute camera (only if self._scaled_surface = None)
        self._recompute_camera_scale(surface)
        assert self._scaled_surface is not None

        # Render scaled
        pygame.transform.scale(self._final_surface, self._scaled_surface.get_size(), self._scaled_surface)
        surface.blit(self._scaled_surface, self._scaled_surface_pos)

        # Actions keys
        pressed_keys = pygame.key.get_pressed()
        for (key, (player_idx, action)) in KEYS_PLAYERS.items():
            if pressed_keys[key]:
                player_entity = self._stage.get_player(player_idx)
                if player_entity is not None:
                    if action == "left":
                        player_entity.move_left()
                    elif action == "right":
                        player_entity.move_right()
                    elif action == "up":
                        player_entity.move_jump()
                    elif action == "down":
                        player_entity.do_down_action()
                    elif action == "action":
                        player_entity.do_action()
                    elif action == "heavy_action":
                        player_entity.do_heavy_action()

        # Stop running
        if self._stop_running_at is None:
            if self._stage.is_finished():
                self._shared_data.play_sound("sounds/victory.ogg")
                self._stop_running_at = time.monotonic() + 5
        elif time.monotonic() >= self._stop_running_at:
            self._shared_data.get_game().show_view("end")

    def event(self, event: Event):
        super().event(event)


def _lerp_color(from_color: Tuple[int, int, int], to_color: Tuple[int, int, int], ratio: float) -> Tuple[int, int, int]:
    dr = to_color[0] - from_color[0]
    dg = to_color[1] - from_color[1]
    db = to_color[2] - from_color[2]
    return from_color[0] + int(dr * ratio), from_color[1] + int(dg * ratio), from_color[1] + int(db * ratio)
