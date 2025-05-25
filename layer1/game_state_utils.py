import enum
from collections.abc import Callable
from typing import List


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
    effects: List[Callable[[int, int], None]]
