from enum import Enum, auto
from typing import List, Optional, Tuple

from common import EntityFunc
from layer1 import SelectableObject


class TerrainEnum(Enum):
    EMPTY = auto()
    CONCRETE = auto()
    GRASS = auto()
    WATER = auto()


class UnitTypeEnum(Enum):
    CAULDRON = auto()
    BIG_CAULDRON = auto()
    KNIGHT = auto()
    FARMER = auto()


class SelectionTypeEnum(Enum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()


class Tile(SelectableObject):
    def __init__(
        self,
        pos: Tuple[int, int],
        terrain: TerrainEnum,
        /,
        *,
        effects: Optional[List[EntityFunc]] = None,
        unit: Optional[UnitTypeEnum] = None,
    ):
        if effects is None:
            effects = []
        x, y = pos
        self.x = x
        self.y = y
        self.terrain = terrain
        self.effects = effects
        self.unit = unit
