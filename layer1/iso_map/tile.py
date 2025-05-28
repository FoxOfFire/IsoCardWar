from collections.abc import Callable
from enum import Enum, auto
from typing import List, Optional, Tuple

from layer1 import SelectableObject


class TerrainEnum(Enum):
    CONCRETE = auto()
    GRASS = auto()
    WATER = auto()


class UnitTypeEnum(Enum):
    CAULDRON = auto()
    BIG_CAULDRON = auto()
    GUY = auto()


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
        effects: Optional[List[Callable[[int, int], None]]] = None,
        unit: Optional[UnitTypeEnum] = None,
        selection: Optional[SelectionTypeEnum] = None,
    ):
        if effects is None:
            effects = []
        x, y = pos
        self.x = x
        self.y = y
        self.terrain = terrain
        self.effects = effects
        self.unit = unit
        self.selection = selection
