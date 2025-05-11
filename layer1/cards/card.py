import enum


class CardTypeEnum(enum.IntEnum):
    SINGLE_USE = enum.auto()
    BUILDABLE = enum.auto()
    PASSIVE = enum.auto()
