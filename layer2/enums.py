from enum import IntEnum, auto


class WorldEnum(IntEnum):
    GAME = auto()


class UIStateEnum(IntEnum):
    BASE = auto()
    HOVER = auto()
    PRESSED = auto()
