from view.anim import AnimSurfaceColored, AnimTracker
from view.tilemap import TileMap, TERRAIN_TILEMAP
from view import View, ViewObject, controls
from stage import Stage, Tile
from entity import Entity

from typing import Optional, Dict
from abc import ABC, abstractmethod
from pygame import Surface
import pygame


class _EntityDrawer(ABC):

    def __init__(self, entity: Entity, view: 'InGameView'):
        self.entity = entity
        self.view = view

    @abstractmethod
    def draw(self, surface: Surface): ...


class InGameView(View):

    BACKGROUND_COLOR = None

    TILES_NAMES = {
        Tile.TILE_DIRT: "dirt",
        Tile.TILE_GRASS: "grass",
        Tile.TILE_PUDDLE: "puddle",
        Tile.TILE_FARMLAND: "farmland"
    }

    TILE_RENDER_SIZE = 128

    def __init__(self):

        super().__init__()

        self._terrain_tilemap: Optional[TileMap] = None
        self._terrain_surface: Optional[Surface] = None

        self._stage: Optional[Stage] = None

        self._stage_size = (0, 0)
        self._stage_ratio = 0
        self._camera_dirty = False
        self._camera_range = (0, 0)
        self._camera_y = 10

        self._scaled_terrain_surface: Optional[Surface] = None
        self._scaled_terrain_pos = (0, 0)

        self._player_anim_surface: Optional[AnimSurfaceColored] = None
        self._player_anim_trackers: Dict[int, AnimTracker] = {}

        self._entities = {}

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

    # Private #

    def _redraw_terrain(self):

        print("Drawing stage terrain...")

        width, height = self._stage.get_size()
        px_width, px_height = width * self.TILE_RENDER_SIZE, height * self.TILE_RENDER_SIZE

        self._terrain_surface = Surface((px_width, px_height), 0, self._shared_data.get_game().get_surface())

        for x, y, tile_id in self._stage.for_each_tile():
            tile_name = self.TILES_NAMES.get(tile_id)
            if tile_name is not None:
                tile_surface = self._terrain_tilemap.get_tile(tile_name)
                if tile_surface is not None:
                    self._terrain_surface.blit(tile_surface, (x * self.TILE_RENDER_SIZE, px_height - (y + 1) * self.TILE_RENDER_SIZE))

        self._stage_size = (width, height)
        self._stage_ratio = height / width
        self._camera_range = (0, width)
        self._scaled_terrain_surface = None
        self._camera_dirty = True

        print("=> Stage terrain drawn!")

    def _recompute_camera_scale(self, surface: Surface):

        shown_width = min(self._stage_size[0], self._camera_range[1] - self._camera_range[0])
        invert_ratio = self._stage_size[0] / shown_width
        range_start_ratio = self._camera_range[0] / self._stage_size[0]

        surface_width, surface_height = surface.get_size()
        terrain_width = surface_width * invert_ratio
        terrain_height = terrain_width * self._stage_ratio

        self._scaled_terrain_pos = (
            terrain_width * -range_start_ratio,
            (surface_height - terrain_height) / 2
        )

        new_size = (int(terrain_width), int(terrain_height))
        if self._scaled_terrain_surface is None or self._scaled_terrain_surface.get_size() != new_size:
            self._scaled_terrain_surface = pygame.transform.scale(self._terrain_surface, new_size)

        self._camera_dirty = False

    def _on_entity_added(self, entity: Entity):
        print("Entity added: {}".format(entity))

    def _inner_init(self):
        self._terrain_tilemap = self._shared_data.get_tilemap("terrain.png", TERRAIN_TILEMAP)\
            .copy_scaled(self.TILE_RENDER_SIZE, self.TILE_RENDER_SIZE)

    def _inner_pre_draw(self, surface: Surface):

        surface.fill((0, 0, 0))

        if self._camera_dirty:
            self._recompute_camera_scale(surface)

        surface.blit(self._scaled_terrain_surface, self._scaled_terrain_pos)
