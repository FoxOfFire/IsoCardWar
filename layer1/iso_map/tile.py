from enum import IntEnum, auto
from typing import Optional, Tuple


class TerrainEnum(IntEnum):
    EMPTY = auto()
    CONCRETE = auto()
    GRASS = auto()
    WATER = auto()


class UnitTypeEnum(IntEnum):
    CAULDRON = auto()
    BIG_CAULDRON = auto()
    BUSH = auto()
    WITCH = auto()
    KNIGHT = auto()
    FARMER = auto()


class Tile:
    def __init__(
        self,
        pos: Tuple[int, int],
        terrain: TerrainEnum,
        /,
        *,
        unit: Optional[UnitTypeEnum] = None,
    ):
        x, y = pos
        self.x = x
        self.y = y
        self.terrain = terrain
        self.target: Optional[int] = None
        self.unit = unit
