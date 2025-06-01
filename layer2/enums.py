from enum import Enum, auto


class WorldEnum(Enum):
    GAME = "Game"


class UIStateEnum(Enum):
    BASE = auto()
    HOVER = auto()
    PRESSED = auto()
