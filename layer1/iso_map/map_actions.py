import esper

from common import Action, ActionArgs

from .log import logger
from .tile import TerrainEnum, Tile, UnitTypeEnum


def get_change_tile_to_action(terrain: TerrainEnum) -> Action:
    def change(args: ActionArgs) -> None:
        assert args is not None
        ent, target = args
        assert target is not None
        tile = esper.component_for_entity(target, Tile)
        tile.terrain = terrain
        logger.info(tile.terrain)

    fn = change
    return fn


def change_tile(args: ActionArgs) -> None:
    assert args is not None
    ent, target = args
    assert target is not None
    tile = esper.component_for_entity(target, Tile)
    terrain = TerrainEnum(tile.terrain.value % len(list(TerrainEnum)) + 1)
    get_change_tile_to_action(terrain)((ent, target))


def change_unit(args: ActionArgs) -> None:
    assert args is not None
    ent, target = args
    assert target is not None
    tile = esper.component_for_entity(target, Tile)
    logger.info(tile.terrain)
    n = tile.unit.value if tile.unit is not None else 0
    n = (n + 1) % (len(list(UnitTypeEnum)) + 1)
    unit = None if n == 0 else UnitTypeEnum(n)
    tile.unit = unit
