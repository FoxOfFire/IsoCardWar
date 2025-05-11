import enum


class WorldEnum(enum.StrEnum):
    GAME = "Game"


class UIStateEnum(enum.IntEnum):
    BASE = enum.auto()
    HOVER = enum.auto()
    PRESSED = enum.auto()
