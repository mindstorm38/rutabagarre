from view import View, ViewObject, controls
from view.tilemap import TileMap, TERRAIN_TILEMAP
from stage import Tile

from typing import Optional
from pygame import Surface
import pygame


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
        self._resized_terrain_surface: Optional[Surface] = None

        self._stage_width = 0
        self._stage_ratio = 0
        self._camera_range = (0, 0)
        self._camera_scale_rect = (0, 0, 0, 0)

    def on_enter(self):
        self._redraw_terrain()

    def on_quit(self):
        pass

    # Private #

    def _redraw_terrain(self):

        print("Drawing stage terrain...")

        game = self._shared_data.get_game()
        stage = game.get_stage()

        if stage is None:
            print("=> No stage ready in the game.")
            return

        width, height = stage.get_size()
        px_width, px_height = width * self.TILE_RENDER_SIZE, height * self.TILE_RENDER_SIZE

        self._terrain_surface = Surface((px_width, px_height), 0, self._shared_data.get_game().get_surface())

        for x, y, tile_id in stage.for_each_tile():
            tile_name = self.TILES_NAMES.get(tile_id)
            if tile_name is not None:
                tile_surface = self._terrain_tilemap.get_tile(tile_name)
                if tile_surface is not None:
                    self._terrain_surface.blit(tile_surface, (x * self.TILE_RENDER_SIZE, px_height - (y + 1) * self.TILE_RENDER_SIZE))

        self._stage_width = width
        self._stage_ratio = height / width
        self._camera_range = (6, 24)

        print("=> Stage terrain drawn!")

    def _recompute_camera_scale(self):
        # TODO
        pass

    def _inner_init(self):
        self._terrain_tilemap = self._shared_data.get_tilemap("terrain.png", TERRAIN_TILEMAP)\
            .copy_scaled(self.TILE_RENDER_SIZE, self.TILE_RENDER_SIZE)

    def _inner_pre_draw(self, surface: Surface):

        surface.fill((0, 0, 0))

        shown_width = min(self._stage_width, self._camera_range[1] - self._camera_range[0])
        invert_ratio = self._stage_width / shown_width
        range_start_ratio = self._camera_range[0] / self._stage_width

        surface_width, surface_height = surface.get_size()
        terrain_width = surface_width * invert_ratio
        terrain_height = terrain_width * self._stage_ratio

        terrain_x = terrain_width * -range_start_ratio

        scaled_terrain = pygame.transform.scale(self._terrain_surface, (int(terrain_width), int(terrain_height)))
        surface.blit(scaled_terrain, (terrain_x, 0))
