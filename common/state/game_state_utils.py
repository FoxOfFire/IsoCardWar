from enum import Enum, auto
from typing import Callable, List, Optional

Action = Callable[[Optional[int], Optional[int]], None]
TextFunc = Callable[[], str]


def ActionDecor(func: Action) -> Action:
    return func


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


class SelectableObject:
    effects: List[Action]
