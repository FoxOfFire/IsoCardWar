import enum
from collections.abc import Callable
from typing import List, Optional

from layer1 import SelectableObject


class TerrainEnum(enum.Enum):
    CONCRETE = enum.auto()
    GRASS = enum.auto()


class UnitEnum(enum.Enum):
    TANK = enum.auto()


class Tile(SelectableObject):
    def __init__(
        self,
        x: int,
        y: int,
        terrain: TerrainEnum,
        effects: List[Callable[[int, int], None]],
        unit: Optional[UnitEnum] = None,
    ):
        self.x = x
        self.y = y
        self.terrain = terrain
        self.effects = effects
        self.unit = unit
