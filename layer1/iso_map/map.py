from random import randint
from typing import Optional, Tuple, Type

import esper

from common import BoundingBox, Untracked

from .tile import TerrainEnum, Tile, UnitTypeEnum


class MapData:
    def __init__(self) -> None:
        self.tracker_tag: Optional[Type] = None
        self.sprite: Optional[Type] = None
        self.size: Optional[Tuple[int, int]] = None


map_obj = MapData()


def make_map() -> None:
    if (
        map_obj.tracker_tag is None
        or map_obj.sprite is None
        or map_obj.size is None
    ):
        raise RuntimeError(
            "failed to fetch map data of tracker:\t"
            + f"{map_obj.tracker_tag}, sprite:{map_obj.sprite} "
            + f"or size:{map_obj.size}"
        )
    w, h = map_obj.size
    tracker = map_obj.tracker_tag
    sprite = map_obj.sprite
    for i in range(h):
        for j in range(w):
            bb = BoundingBox(i, i + 1, j, j + 1)
            pos = (round(bb.left), round(bb.top))
            terrain = TerrainEnum(randint(1, len(list(TerrainEnum))))
            unit: Optional[UnitTypeEnum] = None

            if (
                randint(0, 2) == 0
                and terrain != TerrainEnum.WATER
                and terrain != TerrainEnum.EMPTY
            ):
                unit = UnitTypeEnum(randint(1, len(list(UnitTypeEnum))))

            tile = Tile(pos, terrain, unit=unit)

            esper.create_entity(bb, sprite(), tracker(), tile, Untracked())
