from entity.motion_entity.player import PlayerColor
from typing import Tuple


DEFAULT_PLAYER_COLOR = 255, 255, 255
ORDERED_PLAYER_COLORS = [
    (PlayerColor.RED, (226, 15, 0)),
    (PlayerColor.ORANGE, (242, 133, 0)),
    (PlayerColor.YELLOW, (255, 255, 0)),
    (PlayerColor.GREEN, (84, 194, 66)),
    (PlayerColor.BLUE, (30, 64, 114)),
    (PlayerColor.VIOLET, (113, 86, 150))
]
PLAYER_COLORS = {enum.value: col for enum, col in ORDERED_PLAYER_COLORS}


def get_player_color(enum: PlayerColor) -> Tuple[int, int, int]:
    return PLAYER_COLORS.get(enum.value, DEFAULT_PLAYER_COLOR)
