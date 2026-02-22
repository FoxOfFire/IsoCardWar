from enum import IntEnum, auto


class OrganizationEnum(IntEnum):
    NONE = auto()
    NAME = auto()


class CardTypeEnum(IntEnum):
    DRAW = auto()
    CHANGE_TERRAIN = auto()
    REMOVE_UNIT = auto()
    CAULDRON = auto()
    BIG_CAULDRON = auto()
    BUSH = auto()
