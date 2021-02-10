from typing import Optional, Callable

from pygame.event import Event
from pygame import Surface
import pygame

from . import ViewObject, View


ActionCallback = Optional[Callable[[ViewObject], None]]


class ViewButton(ViewObject):

    """
    Bouton pouvant être utilisé par les vues, doit être créé dans `View.init` au plus tôt en
    fournissant la fonte et le texte. Il faut également définir sa position et sa taille.
    """

    def __init__(self, font_size: int, text: str, *, disabled: bool = False):

        super().__init__(300, 50)

        self._font_size = font_size
        self._text = text
        self._disabled = disabled

        self._text_surface: Optional[Surface] = None
        self._text_pos = (0, 0)

        self._over = False
        self._action_cb: ActionCallback = None

    def set_position(self, x: float, y: float):
        super().set_position(x, y)
        self._refresh_text_pos()

    def set_size(self, width: float, height: float):
        super().set_size(width, height)
        self._refresh_text_pos()

    def set_disabled(self, disabled: bool):
        self._disabled = disabled

    def set_action_callback(self, callback: ActionCallback):
        self._action_cb = callback

    # Private #

    def _redraw(self):
        if self.in_view():
            self._text_surface = self._get_font(self._font_size).render(self._text, True, self._view.TEXT_COLOR)
            self._refresh_text_pos()

    def _refresh_text_pos(self):
        if self.in_view():
            rect = self._text_surface.get_rect()
            self._text_pos = (
                self._pos[0] + (self._size[0] - rect.width) / 2,
                self._pos[1] + (self._size[1] - rect.height) / 2
            )

    def _get_color(self):
        return self._view.BUTTON_OVER_COLOR if self._over and not self._disabled else self._view.BUTTON_NORMAL_COLOR

    # Méthodes override #

    def draw(self, surface: Surface):
        if self.in_view():
            pygame.draw.rect(surface, self._get_color(), self._pos + self._size, 0, 5)
            surface.blit(self._text_surface, self._text_pos)

    def event(self, event: Event):
        if event.type == pygame.MOUSEMOTION:
            self._over = self.is_cursor_over(*event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._over and self._action_cb is not None:
                self._action_cb(self)

    def set_view(self, view: View):
        super().set_view(view)
        self._redraw()
