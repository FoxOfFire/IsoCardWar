import enum


class OrganizationEnum(enum.Enum):
    NONE = enum.auto()
    NAME = enum.auto()
    MARKER = enum.auto()


class CardTypeEnum(enum.Enum):
    DRAW_ONE = "Supply lines"
    CHANGE_TERRAIN_AND_DRAW = "Terrain"
    CHANGE_UNIT_AND_DRAW = "Unit"
