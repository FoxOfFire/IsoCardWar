from enum import IntEnum, auto


class OrganizationEnum(IntEnum):
    NONE = auto()
    NAME = auto()
    MARKER = auto()


class CardTypeEnum(IntEnum):
    DRAW_ONE = auto()
    CHANGE_TERRAIN_AND_DRAW = auto()
    CHANGE_UNIT_AND_DRAW = auto()
