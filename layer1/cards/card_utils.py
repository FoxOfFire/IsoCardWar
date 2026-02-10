from enum import Enum, auto


class OrganizationEnum(Enum):
    NONE = auto()
    NAME = auto()
    MARKER = auto()


class CardTypeEnum(Enum):
    DRAW_ONE = "Supply lines"
    CHANGE_TERRAIN_AND_DRAW = "Terrain"
    CHANGE_UNIT_AND_DRAW = "Unit"
