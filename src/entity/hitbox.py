from __future__ import annotations


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

    # SETTERS
    def set_positions(self, min_x: float, min_y: float, max_x: float, max_y: float) -> None:
        self._min_x = min_x
        self._min_y = min_y
        self._max_x = max_x
        self._max_y = max_y

    def set_min_x(self, min_x: float) -> None:
        self._min_x = min_x

    def set_min_y(self, min_y: float) -> None:
        self._min_y = min_y

    def set_max_x(self, max_x: float) -> None:
        self._max_x = max_x

    def set_max_y(self, max_y: float) -> None:
        self._max_y = max_y

    # OTHER METHODS
    def copy(self) -> Hitbox:
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

    def intersects(self, other_hitbox: Hitbox) -> bool:
        return self.intersects_x(other_hitbox) or self.intersects_y(other_hitbox)

    def intersects_x(self, other_hitbox: Hitbox) -> bool:
        """
        :return: if other_hitbox intersects with this one
        """
        return not (
            other_hitbox._max_x >= self._min_x or
            other_hitbox._min_x <= self._max_x
        )

    def intersects_y(self, other_hitbox: Hitbox) -> bool:
        """
        :return: if other_hitbox intersects with this one
        """
        return not (
            other_hitbox._max_y <= self._min_y or
            other_hitbox._min_y >= self._max_y
        )

    def calc_offset_x(self, other_hitbox: Hitbox, x: float) -> float:
        """
        Calculates how far we can move among the x-axis without hitting other_hitbox.
        Supposes that else we we hit other_hitbox
        :return: `x +/- (what is necessary to be able to move)`
        """
        if x > 0:
            # We go right
            return other_hitbox._min_x - self._max_x
        elif x < 0:
            # We go left
            return other_hitbox._max_x - self._min_x
        else:
            raise ValueError("Error: it's abnormal to calculate the offset when x = 0: something goes wrong")

    def calc_offset_y(self, other_hitbox: Hitbox, y: float) -> float:
        """
        Calculates how far we can move among the y-axis without hitting other_hitbox.
        Supposes that else we we hit other_hitbox
        :return: `y +/- (what is necessary to be able to move)`
        """
        if y > 0:
            # We go up
            return other_hitbox._min_y - self._max_y
        elif y < 0:
            # We go down
            return other_hitbox._max_y - self._min_y
        else:
            raise ValueError("Error: it's abnormal to calculate the offset when y = 0: something goes wrong")
