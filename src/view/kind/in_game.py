from view.anim import AnimSurfaceColored, AnimSurface, AnimTracker, FARMER_ANIMATION, POTATO_ANIMATION, EFFECTS_ANIMATION
from view.tilemap import TileMap, TERRAIN_TILEMAP, ITEMS_TILEMAP
from view.player import get_player_color
from view.controls import KEYS_PLAYERS
from stage import Stage, Tile
from view import View

from entity.player import Player, IncarnationType
from entity.effect import Effect, EffectType
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

    DEBUG_HITBOXES = True

    def __init__(self, entity: Entity, view: 'InGameView', size: Tuple[int, int]):
        self.entity = entity
        self.view = view
        self.offsets = (-int(size[0] / 2), -size[1])

    @classmethod
    def undefined_drawer(cls, entity: Entity, view: 'InGameView'):
        return cls(entity, view, (0, 0))

    def get_draw_pos(self) -> Tuple[int, int]:
        x, y = self.view.get_screen_pos(self.entity.get_x(), self.entity.get_y())
        return x + self.offsets[0], y + self.offsets[1]

    def get_bounding_draw_rect(self) -> Tuple[int, int, int, int]:
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

    __slots__ = "color", "tracker", "rev", "bar_phase_shift", "camera_x"

    BAR_WIDTH, BAR_HEIGHT = 150, 10
    BAR_OFFSET = 40
    HALF_BAR_WIDTH = BAR_WIDTH // 2
    HEALTH_BACKGROUND_COLOR = 16, 26, 11
    MAX_HEALTH_COLOR = 74, 201, 20
    MIN_HEALTH_COLOR = 201, 20, 20
    CAMERA_SPEED = 0.1

    def __init__(self, entity: Player, view: 'InGameView'):
        super().__init__(entity, view, (InGameView.PLAYER_SIZE, InGameView.PLAYER_SIZE))
        self.color = get_player_color(entity.get_color())
        self.tracker = AnimTracker()
        self.tracker.push_infinite_anim("idle", 7)
        self.rev = False
        self.bar_phase_shift = random.random() * math.pi
        self.camera_x = entity.get_x()

    def get_camera_x(self) -> Optional[float]:
        return self.camera_x

    def draw(self, surface: Surface):

        player = cast(Player, self.entity)

        if self.rev != player.get_turned_to_left():
            self.rev = player.get_turned_to_left()
            self.tracker.set_all_reversed(self.rev)

        mutating = self.tracker.is_last_anim("pick")

        for animation in player.foreach_animation():
            if not mutating:
                if animation == "farmer:rake_attack":
                    self.tracker.push_anim("attack_side", 1, 40, rev=self.rev, ignore_existing=False)
                elif animation == "potato:punch":
                    self.tracker.push_anim("attack_side", 1, 20, rev=self.rev, ignore_existing=False)
                elif animation == "farmer:spinning_attack":
                    self.tracker.push_anim("attack_down", 2, 40, rev=self.rev, ignore_existing=False)
                elif animation == "hit":
                    self.tracker.push_anim("hit", 1, 20, rev=self.rev, ignore_existing=False)
                elif animation == "player:mutation":
                    self.tracker.push_anim("pick", 1, 10, rev=self.rev)
                    mutating = True

        if not mutating and player.get_vel_x() != 0 and player.is_on_ground() and self.tracker.is_last_anim("idle", "run"):
            self.tracker.push_infinite_anim("run", 14, rev=self.rev, ignore_existing=False)
        else:
            self.tracker.stop_last_anim("run")

        anim_surface = None
        if not mutating:
            if player.get_incarnation_type() == IncarnationType.POTATO:
                anim_surface = self.view.get_potato_anim_surface()

        if anim_surface is None:
            anim_surface = self.view.get_player_anim_surface()

        anim_surface.blit_color_on(surface, self.get_draw_pos(), self.tracker, self.color)

        health_ratio = player.get_hp_ratio()
        health_color = _lerp_color(self.MIN_HEALTH_COLOR, self.MAX_HEALTH_COLOR, health_ratio)
        health_bar_x, health_bar_y = self.view.get_screen_pos(self.entity.get_x(), self.entity.get_y())
        health_bar_x -= self.HALF_BAR_WIDTH
        health_bar_y -= InGameView.PLAYER_SIZE + self.BAR_OFFSET + math.cos(time.monotonic() * 6 + self.bar_phase_shift) * 4
        health_bar_width = int(self.BAR_WIDTH * health_ratio)

        pygame.draw.rect(surface, self.HEALTH_BACKGROUND_COLOR, (
            health_bar_x + health_bar_width,
            health_bar_y,
            self.BAR_WIDTH - health_bar_width,
            self.BAR_HEIGHT
        ))

        pygame.draw.rect(surface, health_color, (
            health_bar_x,
            health_bar_y,
            health_bar_width,
            self.BAR_HEIGHT
        ))

        self.camera_x += (player.get_x() - self.camera_x) * self.CAMERA_SPEED


class ItemDrawer(EntityDrawer):

    __slots__ = "tile_surface"

    ITEMS_NAMES = {
        IncarnationType.POTATO: "potato"
    }

    def __init__(self, entity: Item, view: 'InGameView'):
        super().__init__(entity, view, (InGameView.ITEM_SIZE, InGameView.ITEM_SIZE))
        tile_name = self.ITEMS_NAMES.get(entity.get_incarnation_type())
        self.tile_surface = None if tile_name is None else view.get_item_tilemap().get_tile(tile_name)

    def draw(self, surface: Surface):
        if self.tile_surface is not None:
            surface.blit(self.tile_surface, self.get_draw_pos())


class EffectDrawer(EntityDrawer):

    __slots__ = "anim_surface", "tracker", "effect_type"

    DEBUG_HITBOXES = False

    EFFECT_ANIMS = {
        EffectType.SMOKE: ("smoke", 6),
        EffectType.SMALL_GROUND_DUST: ("small_ground_dust", 8),
        EffectType.BIG_GROUND_DUST: ("big_ground_dust", 8),
        EffectType.SLEEPING: ("sleeping_start", 3)
    }

    def __init__(self, entity: Effect, view: 'InGameView'):
        super().__init__(entity, view, (InGameView.EFFECT_SIZE, InGameView.EFFECT_SIZE))
        self.anim_surface = view.get_effect_anim_surface()
        self.tracker = AnimTracker()
        self.effect_type = entity.get_effect_type()
        if self.effect_type in self.EFFECT_ANIMS:
            name, fps = self.EFFECT_ANIMS[self.effect_type]
            self.tracker.push_anim(name, 1, fps)

    def draw(self, surface: Surface):
        self.anim_surface.blit_on(surface, self.get_draw_pos(), self.tracker)


class InGameView(View):

    BACKGROUND_COLOR = None

    TILES_NAMES = {
        Tile.TILE_DIRT: "dirt",
        Tile.TILE_GRASS: "grass",
        Tile.TILE_PUDDLE: "puddle",
        Tile.TILE_FARMLAND: "farmland"
    }

    ENTITY_DRAWERS: Dict[Type[Entity], Callable[[Entity, 'InGameView'], EntityDrawer]] = {
        Player: PlayerDrawer,
        Item: ItemDrawer,
        Effect: EffectDrawer
    }

    TILE_SIZE = 64
    PLAYER_SIZE = 128
    ITEM_SIZE = 128
    EFFECT_SIZE = 128
    CAMERA_MARGIN = 8

    CAMERA_UPDATE_THRESHOLD = 0.02

    def __init__(self):

        super().__init__()

        self._terrain_tilemap: Optional[TileMap] = None
        self._item_tilemap: Optional[TileMap] = None
        self._player_anim_surface: Optional[AnimSurfaceColored] = None
        self._potato_anim_surface: Optional[AnimSurfaceColored] = None
        self._effect_anim_surface: Optional[AnimSurface] = None

        self._stage: Optional[Stage] = None
        self._stage_size = (0, 0)
        self._stage_ratio = 0

        # Surfaces "not-scaled"
        self._terrain_surface: Optional[Surface] = None
        self._final_surface: Optional[Surface] = None
        self._y_offset: int = 0

        self._camera_range = (0, 0, 0)
        self._camera_dirty_pos = False
        self._camera_last_next_update: float = 0

        self._scaled_surface: Optional[Surface] = None
        self._scaled_surface_pos = (0, 0)

        self._entities: Dict[int, EntityDrawer] = {}

    def on_enter(self):

        print("Loading stage...")

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

        self._terrain_surface = Surface(unscaled_size, 0, self._shared_data.get_game().get_surface())
        self._final_surface = Surface(unscaled_size, 0, self._shared_data.get_game().get_surface())

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

            range_width = self._camera_range[2]
            range_invert_ratio = self._stage_size[0] / range_width

            start_ratio = self._camera_range[0] / self._stage_size[0]

            surface_width, surface_height = surface.get_size()

            scaled_size = (
                surface_width * range_invert_ratio,
                surface_width * range_invert_ratio * self._stage_ratio
            )

            if self._scaled_surface is None:
                self._scaled_surface = Surface(scaled_size, 0, self._shared_data.get_game().get_surface())

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

        self._effect_anim_surface = AnimSurface(self.EFFECT_SIZE, self.EFFECT_SIZE, [
            self._shared_data.get_anim("effects.png", EFFECTS_ANIMATION)
        ])

    def _inner_pre_draw(self, surface: Surface):

        surface.fill((0, 0, 0))

        if self._stage is None:
            return

        self._final_surface.fill((0, 0, 0))
        self._final_surface.blit(self._terrain_surface, (0, 0))

        # Camera
        camera_range_min = None
        camera_range_max = None

        for entity_drawer in self._entities.values():
            entity_drawer.draw(self._final_surface)
            if entity_drawer.DEBUG_HITBOXES:
                pygame.draw.rect(self._final_surface, (255, 255, 255, 60), entity_drawer.get_bounding_draw_rect(), 2)
            camera_x = entity_drawer.get_camera_x()
            if camera_x is not None:
                if camera_range_min is None:
                    camera_range_min = camera_range_max = camera_x
                elif camera_range_min > camera_x:
                    camera_range_min = camera_x
                elif camera_range_max < camera_x:
                    camera_range_max = camera_x

        if camera_range_min is None:
            camera_range_max = camera_range_min = self._stage_size[0] / 2

        camera_range_min = min(self._stage_size[0], max(0, camera_range_min)) - self.CAMERA_MARGIN
        camera_range_max = min(self._stage_size[0], max(0, camera_range_max)) + self.CAMERA_MARGIN

        if abs(self._camera_range[0] - camera_range_min) >= self.CAMERA_UPDATE_THRESHOLD or \
           abs(self._camera_range[1] - camera_range_max) >= self.CAMERA_UPDATE_THRESHOLD:
            range_width = camera_range_max - camera_range_min
            if abs(self._camera_range[2] - range_width) >= self.CAMERA_UPDATE_THRESHOLD:
                self._scaled_surface = None
            self._camera_dirty_pos = True
            self._camera_range = (camera_range_min, camera_range_max, camera_range_max - camera_range_min)

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


    def event(self, event: Event):
        super().event(event)


def _lerp_color(from_color: Tuple[int, int, int], to_color: Tuple[int, int, int], ratio: float) -> Tuple[int, int, int]:
    dr = to_color[0] - from_color[0]
    dg = to_color[1] - from_color[1]
    db = to_color[2] - from_color[2]
    return from_color[0] + int(dr * ratio), from_color[1] + int(dg * ratio), from_color[1] + int(db * ratio)
