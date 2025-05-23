import enum
from math import sqrt

CARD_Y_POS = 130
CARD_START_X = 0
CARD_START_Y = 0


CARD_WIDTH: float = 31.0
CARD_HEIGHT: float = 44.0
ROOT_TWO: float = sqrt(2.0)


class PriceEnum(enum.StrEnum):
    AMMO = "Ammo"
    METAL = "Metal"
    FOOD = "Food"


class MarkerEnum(enum.IntEnum):
    ACTION = enum.auto()
    UNIT = enum.auto()
    BUILDING = enum.auto()
    UNIQUE = enum.auto()
