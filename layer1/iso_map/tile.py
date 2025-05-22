import enum
from dataclasses import dataclass
from typing import Optional


class TerrainEnum(enum.Enum):
    CONCRETE = enum.auto()
    GRASS = enum.auto()


class UnitEnum(enum.Enum):
    TANK = enum.auto()


@dataclass
class Tile:
    x: int
    y: int
    terrain: TerrainEnum
    unit: Optional[UnitEnum] = None
