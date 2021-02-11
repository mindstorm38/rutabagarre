from view import View, ViewObject, controls
from view.anim import AnimSurfaceColored, AnimTracker, FARMER_ANIMATION
from view.button import ViewButton
from view.player import ORDERED_PLAYER_COLORS, get_player_color

from typing import Optional, Dict, Tuple, List, Callable
from pygame.event import Event
from pygame import Surface
import pygame

from entity.player import PlayerColor
from stage import Stage
import time


PlayerChangeCallback = Optional[Callable[[int, Optional[PlayerColor]], None]]


class ColorSelectView(View):

    BACKGROUND_COLOR = 133, 43, 24

    def __init__(self):

        super().__init__()

        self._player_anim_surface: Optional[AnimSurfaceColored] = None
        self._player_anim_tracker = AnimTracker()
        self._player_anim_tracker.push_infinite_anim("idle", 4)

        self._title: Optional[ViewButton] = None
        self._color_grid: Optional['ViewColorGrid'] = None
        self._players_slots: List[Tuple[ViewPlayerSlot, int]] = []
        self._players_slots_width = 0

        self._return_button: Optional[ViewButton] = None
        self._how_to_play_button: Optional[ViewButton] = None
        self._start_button: Optional[ViewButton] = None

    def _inner_init(self):

        self._player_anim_surface = self._shared_data.new_anim_colored("farmer", FARMER_ANIMATION, 210, 210)

        self._title = ViewButton(35, "Select your color", disabled=True)
        self.add_child(self._title)

        self._color_grid = ViewColorGrid(100, 2, 7)
        self._color_grid.set_change_callback(self._grid_player_changed)
        self.add_child(self._color_grid)

        self._players_slots_width = 0
        for i, _ in enumerate(controls.PLAYERS_KEYS):
            slot = ViewPlayerSlot(i, self._player_anim_surface, self._player_anim_tracker)
            self.add_child(slot)
            self._players_slots.append((slot, self._players_slots_width))
            self._players_slots_width += slot.get_width()

        self._return_button = ViewButton(35, "Return")
        self._return_button.set_action_callback(self._shared_data.get_show_view_callback("title"))
        self._how_to_play_button = ViewButton(35, "How To Play")
        self._start_button = ViewButton(35, "Start")
        self._start_button.set_action_callback(self._on_start_action)

        self.add_child(self._return_button)
        self.add_child(self._start_button)

    def _inner_pre_draw(self, surface: Surface):

        height = surface.get_height()
        width = surface.get_width()
        x_mid = width / 2

        self._color_grid.set_position_centered(x_mid, 225)
        self._title.set_position_centered(x_mid, 55)

        players_slots_x = x_mid - self._players_slots_width / 2
        for slot, offset in self._players_slots:
            slot.set_position(players_slots_x + offset, 360)

        self._return_button.set_position(20, height - 70)
        self._start_button.set_position(width - self._start_button.get_width() - 20, height - 70)

    def _grid_player_changed(self, player_idx: int, player_color: Optional[PlayerColor]):
        self._players_slots[player_idx][0].set_player_color(player_color)

    def _on_start_action(self, _button):
        stage = Stage.new_example_stage()
        for player_idx, player_color in self._color_grid.get_selections().items():
            stage.add_player(player_idx, player_color)
        self._shared_data.get_game().set_stage(stage)
        self._shared_data.get_game().show_view("in_game")


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

    def remove_player(self, player_idx: int):
        if player_idx in self._players_selections:
            del self._players_selections[player_idx]
            if self._change_cb is not None:
                self._change_cb(player_idx, None)

    def change_player_color(self, player_idx: int, backward: bool) -> bool:

        """ Change la couleur selectionnée par un joueur suivant une direction par rapport à la selection actuelle. """

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

    def get_selections(self) -> Dict[int, PlayerColor]:
        return {idx: ORDERED_PLAYER_COLORS[selection.color_index][0] for idx, selection in self._players_selections.items()}

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
            selection = self._players_selections[player_idx]
            self._update_player_raw(player_idx, selection)
            if self._change_cb is not None:
                self._change_cb(player_idx, ORDERED_PLAYER_COLORS[selection.color_index][0])

    def _update_player_raw(self, player_idx: int, selection: GridSelection):
        selection.pos = self._get_color_offset(selection.color_index)
        selection.text_surface = self._get_font(41).render("P{}".format(player_idx + 1), True, self.SELECTION_TEXT_COLOR)
        selection.text_pos = (
            selection.pos[0] + (self._cell_size - selection.text_surface.get_width()) / 2,
            selection.pos[1] + (self._cell_size - selection.text_surface.get_height()) / 2
        )

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
                    self.remove_player(player_idx)

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
            if action in self._KEY_BUTTONS_OFFSETS:
                self._key_buttons[action] = button = ViewButton(25, pygame.key.name(key).upper())
                button.set_size(32, 32)
                button.set_disabled(True)

        self._player_anim_surface = player_anim_surface
        self._player_anim_tracker = player_anim_tracker
        self._player_anim_pos = (0, 0)

        self._subtitle_surface: Optional[Surface] = None
        self._subtitle_pos = (0, 0)
        self._subtitle_bg_rect = (0, 0, 0, 0)

        self._last_blink = 0
        self._blinking = False

    def set_player_color(self, player_color: Optional[PlayerColor]):
        self._player_color = None if player_color is None else get_player_color(player_color)
        self._redraw_subtitle()

    # Private #

    def _on_shape_changed(self):
        self._redraw()

    def _redraw(self):

        x_mid = self._pos[0] + self._size[0] / 2
        y_bottom = self._pos[1] + self._size[1]

        for action, button in self._key_buttons.items():
            dx, dy = self._KEY_BUTTONS_OFFSETS[action]
            button.set_position_centered(x_mid + dx, y_bottom + dy - 70)

        self._player_anim_pos = (x_mid - self._player_anim_surface.get_width() / 2, self._pos[1] + 10)

        if self._subtitle_surface is not None:

            self._subtitle_pos = (
                x_mid - self._subtitle_surface.get_width() / 2,
                y_bottom - self._subtitle_surface.get_height() - 20
            )

            bg_width = max(100, self._subtitle_surface.get_width() + 20)

            self._subtitle_bg_rect = (
                x_mid - bg_width / 2,
                self._subtitle_pos[1] - 5,
                bg_width,
                self._subtitle_surface.get_height() + 10
            )

    def _redraw_subtitle(self):
        if self.in_view():
            subtitle = "Press to join" if self._player_color is None else "P{}".format(self._player_idx + 1)
            text_color = self._view.TEXT_COLOR if self._player_color is None else (0, 0, 0)
            self._subtitle_surface = self._get_font(25).render(subtitle, True, text_color)

    # Méthodes override #

    def draw(self, surface: Surface):

        # Debug background color
        # pygame.draw.rect(surface, (0, 0, 0), self._pos + self._size)

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

        if self._subtitle_surface is not None:
            color = self._view.BUTTON_NORMAL_COLOR if self._player_color is None else self._player_color
            pygame.draw.rect(surface, color, self._subtitle_bg_rect, 0, 5)
            surface.blit(self._subtitle_surface, self._subtitle_pos)

    def event(self, event: Event):
        pass

    def set_view(self, view: View):

        super().set_view(view)

        for button in self._key_buttons.values():
            button.set_view(view)

        self._redraw_subtitle()
        self._redraw()