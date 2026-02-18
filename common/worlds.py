from dataclasses import dataclass
from enum import IntEnum, auto


class WorldEnum(IntEnum):
    GAME = auto()
    MAIN = auto()


@dataclass
class WorldContainer:
    world: WorldEnum = WorldEnum.GAME


WORLD_REF = WorldContainer()
