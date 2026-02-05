from typing import List

import esper

from common.types import EntityFunc

from .log import logger
from .tile import TerrainEnum, Tile, UnitTypeEnum


def change_tile_to(terrain: TerrainEnum) -> List[EntityFunc]:
    effects: List[EntityFunc] = []

    def change(ent: int, target: int) -> None:
        tile = esper.component_for_entity(target, Tile)
        tile.terrain = terrain

    effects.append(change)
    return effects


def change_tile() -> List[EntityFunc]:
    effects: List[EntityFunc] = []

    def rotate(ent: int, target: int) -> None:
        tile = esper.component_for_entity(target, Tile)
        logger.info(tile.terrain)
        tile.terrain = TerrainEnum(
            tile.terrain.value % len(list(TerrainEnum)) + 1
        )

    effects.append(rotate)

    return effects


def change_unit() -> List[EntityFunc]:
    effects: List[EntityFunc] = []

    def rotate(ent: int, target: int) -> None:
        tile = esper.component_for_entity(target, Tile)
        logger.info(tile.terrain)
        n = tile.unit.value if tile.unit is not None else 0
        n = (n + 1) % (len(list(UnitTypeEnum)) + 1)
        unit = None if n == 0 else UnitTypeEnum(n)
        tile.unit = unit

    effects.append(rotate)

    return effects
