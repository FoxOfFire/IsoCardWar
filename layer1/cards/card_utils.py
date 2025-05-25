import enum


class OrganizationEnum(enum.Enum):
    NONE = enum.auto()
    NAME = enum.auto()
    MARKER = enum.auto()


class CardTypeEnum(enum.Enum):
    DRAW_TWO = "Supply lines"
    TURN_TO_CONCRETE = "Poppy"
    TURN_TO_GRASS = "Gardening"
