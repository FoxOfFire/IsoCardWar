from enum import Enum, auto
from typing import Callable, List, Optional

EntityFunc = Callable[[Optional[int], Optional[int]], None]
Action = Callable[[], None]
TextFunc = Callable[[], str]


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
    effects: List[EntityFunc]
