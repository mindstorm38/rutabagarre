from view.anim import AnimSurfaceColored, AnimTracker, FARMER_ANIMATION
from view.tilemap import TileMap, TERRAIN_TILEMAP
from view import View, ViewObject, controls
from stage import Stage, Tile
from entity.player import Player
from entity import Entity

from typing import Optional, Dict, Type, Callable, Tuple
from abc import ABC, abstractmethod
from pygame import Surface
import pygame


class EntityDrawer(ABC):

    def __init__(self, entity: Entity, view: 'InGameView'):
        self.entity = entity
        self.view = view

    def get_draw_pos(self) -> Tuple[int, int]:
        return self.view.get_screen_pos(self.entity.get_x(), self.entity.get_y())

    @abstractmethod
    def draw(self, surface: Surface): ...

    def __str__(self):
        return "{}<euid: {}>".format(type(self), self.entity.get_uid())


class PlayerDrawer(EntityDrawer):

    def __init__(self, entity: Entity, view: 'InGameView'):
        super().__init__(entity, view)
        self.anim_surface = view.get_player_anim_surface()
        self.tracker = AnimTracker()
        self.tracker.push_infinite_anim("idle", 5)

    def draw(self, surface: Surface):
        self.anim_surface.blit_color_on(surface, self.get_draw_pos(), self.tracker, (255, 255, 255))


class InGameView(View):

    BACKGROUND_COLOR = None

    TILES_NAMES = {
        Tile.TILE_DIRT: "dirt",
        Tile.TILE_GRASS: "grass",
        Tile.TILE_PUDDLE: "puddle",
        Tile.TILE_FARMLAND: "farmland"
    }

    ENTITY_DRAWERS: Dict[Type[Entity], Callable[[Entity, 'InGameView'], EntityDrawer]] = {
        Player: PlayerDrawer
    }

    TILE_SIZE = 64
    PLAYER_SIZE = 128

    def __init__(self):

        super().__init__()

        self._terrain_tilemap: Optional[TileMap] = None

        self._stage: Optional[Stage] = None
        self._stage_size = (0, 0)
        self._stage_ratio = 0

        # Surfaces "not-scaled"
        self._terrain_surface: Optional[Surface] = None
        self._final_surface: Optional[Surface] = None
        self._unscaled_size = (0, 0)

        self._scaled_surface: Optional[Surface] = None
        self._scaled_surface_pos = (0, 0)

        self._player_anim_surface: Optional[AnimSurfaceColored] = None
        self._entities: Dict[int, EntityDrawer] = {}

    def on_enter(self):

        print("Loading stage...")

        game = self._shared_data.get_game()
        self._stage = game.get_stage()

        if self._stage is None:
            print("=> No stage ready in the game.")
        else:

            self._stage.set_new_entity_callback(self._on_entity_added)

            for entity in self._stage.get_entities():
                self._on_entity_added(entity)

            self._redraw_terrain()

            print("=> Stage loaded.")

    def on_quit(self):
        if self._stage is not None:
            self._stage.set_new_entity_callback(None)
            self._stage = None

    def get_player_anim_surface(self) -> Optional[AnimSurfaceColored]:
        return self._player_anim_surface

    def get_screen_pos(self, x: float, y: float) -> Tuple[int, int]:
        return int(x * self.TILE_SIZE), self._unscaled_size[1] - int((y + 1) * self.TILE_SIZE)

    # Private #

    def _redraw_terrain(self):

        print("Drawing stage terrain...")

        width, height = self._stage.get_size()

        self._unscaled_size = (
            width * self.TILE_SIZE,
            height * self.TILE_SIZE
        )

        self._terrain_surface = Surface(self._unscaled_size, 0, self._shared_data.get_game().get_surface())
        self._final_surface = Surface(self._unscaled_size, 0, self._shared_data.get_game().get_surface())

        for x, y, tile_id in self._stage.for_each_tile():
            tile_name = self.TILES_NAMES.get(tile_id)
            if tile_name is not None:
                tile_surface = self._terrain_tilemap.get_tile(tile_name)
                if tile_surface is not None:
                    self._terrain_surface.blit(tile_surface, (x * self.TILE_SIZE, self._unscaled_size[1] - (y + 1) * self.TILE_SIZE))

        self._stage_size = (width, height)
        self._stage_ratio = height / width

        print("=> Stage terrain drawn!")

    def _recompute_camera_scale(self, surface: Surface):
        if self._scaled_surface is None:
            surface_width, surface_height = surface.get_size()
            scaled_size = (surface_width, surface_width * self._stage_ratio)
            self._scaled_surface = Surface(scaled_size, 0, self._shared_data.get_game().get_surface())
            self._scaled_surface_pos = (0, (surface_height - scaled_size[1]) / 2)

    def _on_entity_added(self, entity: Entity):
        print("Entity added to view: {}".format(entity))
        constructor = self.ENTITY_DRAWERS.get(type(entity))
        if constructor is not None:
            try:
                drawer = constructor(entity, self)
                self._entities[entity.get_uid()] = drawer
            except (Exception,) as e:
                print("Failed to construct {}: {}".format(constructor, e))

    def _inner_init(self):

        self._terrain_tilemap = self._shared_data.get_tilemap("terrain.png", TERRAIN_TILEMAP)\
            .copy_scaled(self.TILE_SIZE, self.TILE_SIZE)

        self._player_anim_surface = self._shared_data.new_anim_colored("farmer", FARMER_ANIMATION, self.PLAYER_SIZE, self.PLAYER_SIZE)

    def _inner_pre_draw(self, surface: Surface):

        surface.fill((0, 0, 0))

        self._recompute_camera_scale(surface)

        self._final_surface.fill((0, 0, 0))
        self._final_surface.blit(self._terrain_surface, (0, 0))

        for entity_drawer in self._entities.values():
            entity_drawer.draw(self._final_surface)

        pygame.transform.scale(self._final_surface, self._scaled_surface.get_size(), self._scaled_surface)
        surface.blit(self._scaled_surface, self._scaled_surface_pos)