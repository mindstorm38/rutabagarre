from view import View, ViewObject, controls
from view.anim import AnimSurfaceColored, AnimTracker, FARMER_ANIMATION
from view.button import ViewButton
from view.player import ORDERED_PLAYER_COLORS, get_player_color

from typing import Optional, Dict, Tuple, List, Callable
from pygame.event import Event
from pygame import Surface
import pygame

from entity.player import PlayerColor
import time


PlayerChangeCallback = Optional[Callable[[ViewObject, int, PlayerColor], None]]


class ColorSelectView(View):

    BACKGROUND_COLOR = 133, 43, 24

    def __init__(self):

        super().__init__()

        self._player_anim_surface: Optional[AnimSurfaceColored] = None
        self._player_anim_tracker = AnimTracker()
        self._player_anim_tracker.push_infinite_anim("idle", 4)

        self._title_button: Optional[ViewButton] = None
        self._color_grid: Optional['ViewColorGrid'] = None
        self._players_slots: List[Tuple[ViewPlayerSlot, int]] = []
        self._players_slots_width = 0

    def _inner_init(self):

        self._player_anim_surface = self._shared_data.new_anim_colored("farmer", FARMER_ANIMATION, 210, 210)

        self._title_button = ViewButton(35, "Select your color")
        self._title_button.set_disabled(True)
        self.add_child(self._title_button)

        self._color_grid = ViewColorGrid(100, 2, 7)
        self._color_grid.set_change_callback(self._grid_player_changed)
        self.add_child(self._color_grid)

        self._players_slots_width = 0
        for i, _ in enumerate(controls.PLAYERS_KEYS):
            slot = ViewPlayerSlot(i, self._player_anim_surface, self._player_anim_tracker)
            self.add_child(slot)
            self._players_slots.append((slot, self._players_slots_width))
            self._players_slots_width += slot.get_width()

    def _inner_pre_draw(self, surface: Surface):
        x_mid = surface.get_width() / 2
        players_slots_x = x_mid - self._players_slots_width / 2
        self._color_grid.set_position_centered(x_mid, 225)
        self._title_button.set_position_centered(x_mid, 55)
        for slot, offset in self._players_slots:
            slot.set_position(players_slots_x + offset, 360)

    def _grid_player_changed(self, _obj, player_idx: int, player_color: PlayerColor):
        self._players_slots[player_idx][0].set_player_color(player_color)


class GridSelection:
    def __init__(self, color_index: int):
        self.color_index = color_index
        self.pos = (0, 0)
        self.text_surface: Optional[Surface] = None
        self.text_pos = (0, 0)


class ViewColorGrid(ViewObject):

    SELECTION_COLOR = 54, 16, 12
    SELECTION_WIDTH = 5
    SELECTION_TEXT_COLOR = 0, 0, 0

    def __init__(self, cell_size: int, rows: int, columns: int):

        super().__init__(columns * cell_size, rows * cell_size)

        self._cell_size = cell_size
        self._rows = rows
        self._columns = columns

        self._grid_surface: Optional[Surface] = None
        self._selection_surface: Optional[Surface] = None
        self._redraw()

        self._players_selections: Dict[int, GridSelection] = {}

        self._change_cb: PlayerChangeCallback = None

    def insert_player(self, player_idx: int) -> bool:
        if player_idx in self._players_selections:
            return False
        color_idx = self._pick_free_color()
        if color_idx is None:
            return False
        self._players_selections[player_idx] = GridSelection(color_idx)
        self._update_player(player_idx)
        return True

    def change_player_color(self, player_idx: int, backward: bool) -> bool:

        """ Change la couleur selectionné par un joueur suivant une direction par rapport à la selection actuelle. """

        if player_idx not in self._players_selections:
            return False

        selection = self._players_selections[player_idx]
        color_index = selection.color_index
        color_index = self._pick_free_color(start=color_index, inverted=backward)

        if color_index is not None:
            selection.color_index = color_index
            self._update_player(player_idx)
            return True
        else:
            return False


    def set_size(self, width: float, height: float):
        raise ValueError("Cannot set size for this.")

    def set_change_callback(self, callback: PlayerChangeCallback):
        self._change_cb = callback

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
        for idx, (_enum, color_index) in enumerate(ORDERED_PLAYER_COLORS):
            cx, cy = self._get_color_offset(idx)
            pygame.draw.rect(self._grid_surface, color_index, (cx, cy, self._cell_size, self._cell_size))

        self._selection_surface = Surface((self._cell_size, self._cell_size), pygame.SRCALPHA)
        self._selection_surface.fill(self.SELECTION_COLOR)
        pygame.draw.rect(self._selection_surface, (255, 255, 255, 0), (
            self.SELECTION_WIDTH, self.SELECTION_WIDTH,
            self._cell_size - self.SELECTION_WIDTH * 2, self._cell_size - self.SELECTION_WIDTH * 2
        ))

    def _pick_free_color(self, *, start: int = -1, inverted: bool = False) -> Optional[int]:
        idx = start if start >= 0 else len(ORDERED_PLAYER_COLORS) - 1 if inverted else 0
        check = True
        while check:
            check = False
            for selection in self._players_selections.values():
                if selection.color_index == idx:
                    if inverted:
                        idx -= 1
                        if idx < 0:
                            return None
                    else:
                        idx += 1
                        if idx >= len(ORDERED_PLAYER_COLORS):
                            return None
                    check = True
                    break
        return idx

    def _update_player(self, player_idx: int):
        if self.in_view():
            if player_idx not in self._players_selections:
                raise ValueError("The player index {} is not valid.".format(player_idx))
            self._update_player_raw(player_idx, self._players_selections[player_idx])

    def _update_player_raw(self, player_idx: int, selection: GridSelection):
        selection.pos = self._get_color_offset(selection.color_index)
        selection.text_surface = self._get_font(41).render("P{}".format(player_idx + 1), True, self.SELECTION_TEXT_COLOR)
        selection.text_pos = (
            selection.pos[0] + (self._cell_size - selection.text_surface.get_width()) / 2,
            selection.pos[1] + (self._cell_size - selection.text_surface.get_height()) / 2
        )
        if self._change_cb is not None:
            self._change_cb(self, player_idx, ORDERED_PLAYER_COLORS[selection.color_index][0])

    def _get_player_at(self, col: int, row: int) -> Optional[int]:
        color_index = self._get_color_index(col, row)
        for idx, selection in self._players_selections.items():
            if selection.color_index == color_index:
                return idx
        return None

    # Méthodes override #

    def draw(self, surface: Surface):
        surface.blit(self._grid_surface, self._pos)
        x, y = self._pos
        for selection in self._players_selections.values():
            cx, cy = selection.pos
            tx, ty = selection.text_pos
            surface.blit(self._selection_surface, (x + cx, y + cy))
            surface.blit(selection.text_surface, (x + tx, y + ty))

    def event(self, event: Event):
        if event.type == pygame.KEYUP:
            control = controls.KEYS_PLAYERS.get(event.key)
            if control is not None:
                player_idx, action = control
                if action in ("left", "right"):
                    if not self.insert_player(player_idx):
                        self.change_player_color(player_idx, action == "left")
                elif action == "down":
                    # TODO: Remove plus
                    pass

    def set_view(self, view: View):
        super().set_view(view)
        for idx, selection in self._players_selections.items():
            self._update_player_raw(idx, selection)


class ViewPlayerSlot(ViewObject):

    _RES_CONTROLLER = "controller.png"
    _KEY_BUTTONS_OFFSETS = {
        "up": (0, -36),
        "down": (0, 0),
        "left": (-36, 0),
        "right": (36, 0)
    }
    _BLINK_DELAY = 0.4

    def __init__(self, player_idx: int, player_anim_surface: AnimSurfaceColored, player_anim_tracker: AnimTracker):

        super().__init__(240, 280)

        self._player_idx = player_idx
        self._player_color: Optional[Tuple[int, int, int]] = None
        self._controls = controls.PLAYERS_KEYS[player_idx] if player_idx < len(controls.PLAYERS_KEYS) else {}

        self._key_buttons = {}
        for action, key in self._controls.items():
            self._key_buttons[action] = button = ViewButton(25, pygame.key.name(key).upper())
            button.set_size(32, 32)
            button.set_disabled(True)

        self._player_anim_surface = player_anim_surface
        self._player_anim_tracker = player_anim_tracker
        self._player_anim_pos = (0, 0)

        self._last_blink = 0
        self._blinking = False

    def set_player_color(self, player_color: Optional[PlayerColor]):
        self._player_color = None if player_color is None else get_player_color(player_color)

    # Private #

    def _on_shape_changed(self):
        self._redraw()

    def _redraw(self):

        x_mid = self._pos[0] + self._size[0] / 2
        y_bottom = self._pos[1] + self._size[1]

        for action, button in self._key_buttons.items():
            dx, dy = self._KEY_BUTTONS_OFFSETS[action]
            button.set_position_centered(x_mid + dx, y_bottom + dy - 100)

        self._player_anim_pos = (x_mid - self._player_anim_surface.get_width() / 2, self._pos[1] + 10)

    # Méthodes override #

    def draw(self, surface: Surface):

        pygame.draw.rect(surface, (0, 0, 0), self._pos + self._size)

        now = time.monotonic()
        if now - self._last_blink > self._BLINK_DELAY:
            self._last_blink = now
            self._blinking = not self._blinking

        if self._player_color is None:
            for action, button in self._key_buttons.items():
                if action not in ("left", "right") or not self._blinking:
                    button.draw(surface)
        else:
            self._player_anim_surface.blit_color_on(surface, self._player_anim_pos, self._player_anim_tracker, self._player_color)

    def event(self, event: Event):
        pass

    def set_view(self, view: View):

        super().set_view(view)

        for button in self._key_buttons.values():
            button.set_view(view)

        self._redraw()
