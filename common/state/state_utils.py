from enum import Enum, auto
from typing import Callable, Optional, Tuple

ActionArgs = Optional[Tuple[Optional[int], Optional[int]]]
Action = Callable[[ActionArgs], None]
TextFunc = Callable[[], str]


def TextFuncDecor(func: TextFunc) -> TextFunc:
    return func


class MarkerEnum(Enum):
    ACTION = auto()
    UNIT = auto()
    BUILDING = auto()
    UNIQUE = auto()


class PriceEnum(Enum):
    AMMO = "Ammo"
    METAL = "Metal"
    FOOD = "Food"


class GamePhaseEnum(Enum):
    BEGIN_GAME = auto()
    DRAW = auto()
    PLAYER_ACTION = auto()
    END_OF_TURN = auto()
    ENEMY_ACTION = auto()
    END_GAME = auto()
