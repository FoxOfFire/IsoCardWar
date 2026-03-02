from enum import IntEnum, auto
from typing import Callable, Optional

ActionEnt = Optional[int]
Trigger = bool
Action = Callable[[ActionEnt, Trigger], bool]
ActionBase = Callable[[ActionEnt], bool]
TextFunc = Callable[[], str]


def ActionDecor(action_base: ActionBase) -> Action:
    def action(ent: ActionEnt, trig: Trigger) -> bool:
        if not trig:
            return False
        return action_base(ent)

    return action


class PriceEnum(IntEnum):
    MANA = auto()
    HERBS = auto()
    BLOOD = auto()
    BREW = auto()


class GamePhaseType(IntEnum):
    INIT = auto()
    BEGIN_GAME = auto()
    TELEGRAPH = auto()
    PRODUCTION = auto()
    DRAW = auto()
    PLAYER_ACTION = auto()
    END_OF_TURN = auto()
    ENEMY_ACTION = auto()
    END_GAME = auto()
