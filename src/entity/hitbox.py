
class Hitbox:

    """
    Class that defines a rectangular hitbox with absolute position
    """

    def __init__(self, min_x: float, min_y: float, max_x: float, max_y: float) -> None:
        self._min_x: float = min_x
        self._min_y: float = min_y
        self._max_x: float = max_x
        self._max_y: float = max_y

    # GETTERS

    def get_min_x(self) -> float:
        return self._min_x

    def get_min_y(self) -> float:
        return self._min_y

    def get_max_x(self) -> float:
        return self._max_x

    def get_max_y(self) -> float:
        return self._max_y

    def get_width(self) -> float:
        return self._max_x - self._min_x

    def get_height(self) -> float:
        return self._max_y - self._min_y

    def get_mid_x(self) -> float:
        return (self._min_x + self._max_x) / 2

    def get_mid_y(self) -> float:
        return (self._min_y + self._max_y) / 2

    # SETTERS

    def set_positions(self, min_x: float, min_y: float, max_x: float, max_y: float) -> None:
        self._min_x = min_x
        self._min_y = min_y
        self._max_x = max_x
        self._max_y = max_y

    def set_from(self, other: 'Hitbox'):
        self.set_positions(other._min_x, other._min_y, other._max_x, other._max_y)

    def set_min_x(self, min_x: float) -> None:
        self._min_x = min_x

    def set_min_y(self, min_y: float) -> None:
        self._min_y = min_y

    def set_max_x(self, max_x: float) -> None:
        self._max_x = max_x

    def set_max_y(self, max_y: float) -> None:
        self._max_y = max_y

    # OTHER METHODS

    def copy(self) -> 'Hitbox':
        return Hitbox(self._min_x, self._min_y, self._max_x, self._max_y)

    def move(self, x: float, y: float) -> None:
        """
        Moves the hitbox following the vector (x,y)
        """
        self._min_x += x
        self._max_x += x
        self._min_y += y
        self._max_y += y

    def expand(self, x: float, y: float) -> None:
        """
        If x > 0 it expands x from the right-upper angle.
        If y > 0 it expands y from the right-upper angle.
        """
        if x > 0.0:
            self._max_x += x
        else:
            self._min_x += x

        if y > 0.0:
            self._max_y += y
        else:
            self._min_y += y

    def intersects(self, other_hitbox: 'Hitbox') -> bool:
        return (
                self._min_x < other_hitbox._max_x and
                self._max_x > other_hitbox._min_x and
                self._min_y < other_hitbox._max_y and
                self._max_y > other_hitbox._min_y
        )

    def calc_offset_x(self, other_hitbox: 'Hitbox', offset_x: float) -> float:

        if other_hitbox._max_y > self._min_y and other_hitbox._min_y < self._max_y:

            if offset_x > 0.0 and other_hitbox._max_x <= self._min_x:

                d = self._min_x - other_hitbox._max_x

                if d < offset_x:
                    offset_x = d

            elif offset_x < 0.0 and other_hitbox._min_x >= self._max_x:

                d = self._max_x - other_hitbox._min_x

                if d > offset_x:
                    offset_x = d

        return offset_x

    def calc_offset_y(self, other_hitbox: 'Hitbox', offset_y: float) -> float:

        if other_hitbox._max_x > self._min_x and other_hitbox._min_x < self._max_x:

            if offset_y > 0.0 and other_hitbox._max_y <= self._min_y:

                d = self._min_y - other_hitbox._max_y

                if d < offset_y:
                    offset_y = d

            elif offset_y < 0.0 and other_hitbox._min_y >= self._max_y:

                d = self._max_y - other_hitbox._min_y

                if d > offset_y:
                    offset_y = d

        return offset_y
