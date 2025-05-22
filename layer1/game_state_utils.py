import enum
from collections.abc import Callable


class GameStateEnum(enum.Enum):
    SELECT_CARD = enum.auto()
    SELECT_TILE = enum.auto()


class MarkerEnum(enum.IntEnum):
    ACTION = enum.auto()
    UNIT = enum.auto()
    BUILDING = enum.auto()
    UNIQUE = enum.auto()


class PriceEnum(enum.StrEnum):
    AMMO = "Ammo"
    METAL = "Metal"
    FOOD = "Food"


class SelectableObject:
    effect: Callable[[int], None]
