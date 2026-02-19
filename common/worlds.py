from dataclasses import dataclass
from enum import IntEnum, auto
from typing import NamedTuple


class WorldEnum(IntEnum):
    GAME = auto()
    MAIN = auto()


class TempObjectTag(NamedTuple):
    pass


@dataclass
class WorldContainer:
    world: WorldEnum = WorldEnum.GAME


WORLD_REF = WorldContainer()
