from enum import IntEnum, auto
from typing import Callable, Optional

ActionArgs = Optional[int]
Action = Callable[[ActionArgs], None]
TextFunc = Callable[[], str]


class PriceEnum(IntEnum):
    MANA = auto()
    HERBS = auto()
    BLOOD = auto()
    BREW = auto()


class GamePhaseType(IntEnum):
    BEGIN_GAME = auto()
    TELEGRAPH = auto()
    PRODUCTION = auto()
    DRAW = auto()
    PLAYER_ACTION = auto()
    END_OF_TURN = auto()
    ENEMY_ACTION = auto()
    END_GAME = auto()
