from enum import IntEnum, auto
from typing import Callable, Optional

ActionArgs = Optional[int]
Action = Callable[[ActionArgs], None]
TextFunc = Callable[[], str]


def TextFuncDecor(func: TextFunc) -> TextFunc:
    return func


class MarkerEnum(IntEnum):
    ACTION = auto()
    UNIT = auto()
    TERRAIN = auto()
    UNIQUE = auto()


class PriceEnum(IntEnum):
    MANA = auto()
    HERBS = auto()
    BLOOD = auto()


class GamePhaseType(IntEnum):
    BEGIN_GAME = auto()
    DRAW = auto()
    PLAYER_ACTION = auto()
    END_OF_TURN = auto()
    ENEMY_ACTION = auto()
    END_GAME = auto()
