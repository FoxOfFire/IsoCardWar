from typing import Optional

import esper

from common import Action, ActionDecor

from .log import logger
from .tile import TerrainEnum, Tile, UnitTypeEnum


def change_tile_to(terrain: TerrainEnum) -> Action:
    @ActionDecor
    def change(ent: Optional[int], target: Optional[int]) -> None:
        assert target is not None
        tile = esper.component_for_entity(target, Tile)
        tile.terrain = terrain
        logger.info(tile.terrain)

    fn = change
    return fn


@ActionDecor
def change_tile(ent: Optional[int], target: Optional[int]) -> None:
    assert target is not None
    tile = esper.component_for_entity(target, Tile)
    terrain = TerrainEnum(tile.terrain.value % len(list(TerrainEnum)) + 1)
    change_tile_to(terrain)(ent, target)


@ActionDecor
def change_unit(ent: Optional[int], target: Optional[int]) -> None:
    assert target is not None
    tile = esper.component_for_entity(target, Tile)
    logger.info(tile.terrain)
    n = tile.unit.value if tile.unit is not None else 0
    n = (n + 1) % (len(list(UnitTypeEnum)) + 1)
    unit = None if n == 0 else UnitTypeEnum(n)
    tile.unit = unit
