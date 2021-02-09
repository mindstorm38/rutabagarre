from view import View, SharedViewData
from view.button import ViewButton

from typing import Optional, Dict, Tuple
from pygame.event import Event
from pygame.font import Font
from pygame import Surface
import pygame

from entity.motion_entity.player import PlayerColor
from ..controls import KEYS_PLAYERS
from .. import ViewObject


_PLAYER_COLORS = [
    (PlayerColor.RED, (226, 15, 0)),
    (PlayerColor.ORANGE, (242, 133, 0)),
    (PlayerColor.YELLOW, (255, 255, 0)),
    (PlayerColor.GREEN, (84, 194, 66)),
    (PlayerColor.BLUE, (30, 64, 114)),
    (PlayerColor.VIOLET, (113, 86, 150))
]


class ColorSelectView(View):

    BACKGROUND_COLOR = 133, 43, 24

    def __init__(self):
        super().__init__()
        self._color_grid: Optional[ColorGrid] = None
        self._title_button: Optional[ViewButton] = None

    def init(self, data: 'SharedViewData'):

        self._color_grid = ColorGrid(100, 2, 7, data.get_font(41))
        self.add_child(self._color_grid)

        self._title_button = ViewButton(data.get_font(35), "Select your color")
        self._title_button.set_disabled(True)
        self.add_child(self._title_button)

    def draw(self, surface: Surface):
        x_mid = surface.get_width() / 2
        self._color_grid.set_position_centered(x_mid, 225)
        self._title_button.set_position_centered(x_mid, 55)
        super().draw(surface)


class GridSelection:
    def __init__(self, color_index: int):
        self.color_index = color_index
        self.pos = (0, 0)
        self.text_surface: Optional[Surface] = None
        self.text_pos = (0, 0)


class ColorGrid(ViewObject):

    SELECTION_COLOR = 54, 16, 12
    SELECTION_WIDTH = 5
    SELECTION_TEXT_COLOR = 0, 0, 0

    def __init__(self, cell_size: int, rows: int, columns: int, font: Font):

        self._cell_size = cell_size
        self._rows = rows
        self._columns = columns
        self._font = font

        super().__init__(columns * cell_size, rows * cell_size)

        self._grid_surface: Optional[Surface] = None
        self._selection_surface: Optional[Surface] = None
        self._redraw()

        self._players_colors: Dict[int, GridSelection] = {}

        self.insert_player(0)

    def insert_player(self, player_idx: int) -> bool:
        if player_idx in self._players_colors:
            return False
        color = self._pick_free_color()
        if color is None:
            return False
        self._players_colors[player_idx] = GridSelection(color)
        self._update_player(player_idx)
        return True

    def change_player_color(self, player_idx: int, backward: bool) -> bool:

        """ Change la couleur selectionné par un joueur suivant une direction par rapport à la selection actuelle. """

        if player_idx not in self._players_colors:
            return False

        selection = self._players_colors[player_idx]
        color_index = selection.color_index
        print("color_index: {}, backward: {}".format(color_index, backward))
        color_index = self._pick_free_color(start=color_index, inverted=backward)
        print("color_index: {}".format(color_index))
        if color_index is not None:
            selection.color_index = color_index
            self._update_player(player_idx)
            return True
        else:
            return False


    def set_size(self, width: float, height: float):
        raise ValueError("Cannot set size for this.")

    # Private #

    def _get_color_cell(self, color_index: int) -> Tuple[int, int]:
        return color_index % self._columns, color_index // self._columns

    def _get_color_offset(self, color_index: int) -> Tuple[int, int]:
        col, row = self._get_color_cell(color_index)
        return col * self._cell_size, row * self._cell_size

    def _get_color_index(self, col: int, row: int) -> int:
        return col + row * self._columns

    def _redraw(self):

        self._grid_surface = Surface(self._size)
        self._grid_surface.fill((0, 0, 0))
        for idx, (_enum, color_index) in enumerate(_PLAYER_COLORS):
            cx, cy = self._get_color_offset(idx)
            pygame.draw.rect(self._grid_surface, color_index, (cx, cy, self._cell_size, self._cell_size))

        self._selection_surface = Surface((self._cell_size, self._cell_size), pygame.SRCALPHA)
        self._selection_surface.fill(self.SELECTION_COLOR)
        pygame.draw.rect(self._selection_surface, (255, 255, 255, 0), (
            self.SELECTION_WIDTH, self.SELECTION_WIDTH,
            self._cell_size - self.SELECTION_WIDTH * 2, self._cell_size - self.SELECTION_WIDTH * 2
        ))

    def _pick_free_color(self, *, start: int = -1, inverted: bool = False) -> Optional[int]:
        idx = start if start >= 0 else len(_PLAYER_COLORS) - 1 if inverted else 0
        check = True
        while check:
            check = False
            for selection in self._players_colors.values():
                if selection.color_index == idx:
                    if inverted:
                        idx -= 1
                        if idx < 0:
                            return None
                    else:
                        idx += 1
                        if idx >= len(_PLAYER_COLORS):
                            return None
                    check = True
                    break
        return idx

    def _update_player(self, player_idx: int):
        if player_idx not in self._players_colors:
            raise ValueError("The player index {} is not valid.".format(player_idx))
        selection = self._players_colors[player_idx]
        color_index = selection.color_index
        selection.pos = self._get_color_offset(color_index)
        selection.text_surface = self._font.render("P{}".format(player_idx + 1), True, self.SELECTION_TEXT_COLOR)
        selection.text_pos = (
            selection.pos[0] + (self._cell_size - selection.text_surface.get_width()) / 2,
            selection.pos[1] + (self._cell_size - selection.text_surface.get_height()) / 2
        )

    def _get_player_at(self, col: int, row: int) -> Optional[int]:
        color_index = self._get_color_index(col, row)
        for idx, selection in self._players_colors.items():
            if selection.color_index == color_index:
                return idx
        return None

    # Méthodes override #

    def draw(self, surface: Surface):
        surface.blit(self._grid_surface, self._pos)
        x, y = self._pos
        for selection in self._players_colors.values():
            cx, cy = selection.pos
            tx, ty = selection.text_pos
            surface.blit(self._selection_surface, (x + cx, y + cy))
            surface.blit(selection.text_surface, (x + tx, y + ty))

    def event(self, event: Event):
        if event.type == pygame.KEYUP:
            control = KEYS_PLAYERS.get(event.key)
            if control is not None:
                player_idx, action = control
                if action in ("left", "right"):
                    if not self.insert_player(player_idx):
                        self.change_player_color(player_idx, action == "left")
