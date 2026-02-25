from dataclasses import dataclass
from enum import IntEnum, auto
from typing import Optional, Tuple

from common import SETTINGS_REF


class TerrainEnum(IntEnum):
    EMPTY = auto()
    CONCRETE = auto()
    GRASS = auto()
    WATER = auto()


class UnitTypeEnum(IntEnum):
    CAULDRON = auto()
    BIG_CAULDRON = auto()
    BLOOD_BUCKET = auto()
    MANA_PYLON = auto()
    BUSH = auto()
    WITCH = auto()
    KNIGHT = auto()
    FARMER = auto()


@dataclass
class Tile:
    x: int
    y: int
    terrain: TerrainEnum
    target: Optional[int] = None
    unit: Optional[UnitTypeEnum] = None
    is_targeted: bool = False

    @property
    def x_offset(self) -> int:
        return (
            SETTINGS_REF.ISO_POS_OFFSET_X
            + (self.x + self.y) * SETTINGS_REF.ISO_TILE_OFFSET_X
        )

    @property
    def y_offset(self) -> int:
        return (
            SETTINGS_REF.ISO_POS_OFFSET_Y
            + (self.x - self.y - 2) * SETTINGS_REF.ISO_TILE_OFFSET_Y
        )

    @property
    def offset(self) -> Tuple[int, int]:
        return self.x_offset, self.y_offset
