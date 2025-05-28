import enum


class OrganizationEnum(enum.Enum):
    NONE = enum.auto()
    NAME = enum.auto()
    MARKER = enum.auto()


class CardTypeEnum(enum.Enum):
    DRAW_FOUR = "Supply lines"
    CHANGE_SELECTION = "Select"
    CHANGE_TERRAIN = "Poppy"
    CHANGE_UNIT = "Gardening"
