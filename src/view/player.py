from entity.player import PlayerColor
from typing import Tuple


DEFAULT_PLAYER_COLOR = 255, 255, 255
ORDERED_PLAYER_COLORS = [
    (PlayerColor.RED, (226, 15, 0)),
    (PlayerColor.BROWN, (173, 66, 60)),
    (PlayerColor.ORANGE, (242, 133, 0)),
    (PlayerColor.YELLOW, (255, 255, 0)),
    (PlayerColor.GREEN, (84, 194, 66)),
    (PlayerColor.LIGHT_BLUE, (79, 144, 214)),
    (PlayerColor.BLUE, (30, 64, 114)),
    (PlayerColor.PINK, (250, 116, 112)),
    (PlayerColor.LIGHT_BROWN, (210, 139, 135)),
    (PlayerColor.LIGHT_ORANGE, (247, 186, 123)),
    (PlayerColor.CHARTREUSE, (127, 255, 0)),
    (PlayerColor.PALE_GREEN, (167, 224, 165)),
    (PlayerColor.CYAN, (134, 199, 212)),
    (PlayerColor.VIOLET, (113, 86, 150))
]
PLAYER_COLORS = {enum.value: col for enum, col in ORDERED_PLAYER_COLORS}


def get_player_color(enum: PlayerColor) -> Tuple[int, int, int]:
    return PLAYER_COLORS.get(enum.value, DEFAULT_PLAYER_COLOR)
