from typing import Optional, Tuple

import esper

from common import Action, ActionArgs

from .log import logger
from .map import MAP_DATA_REF
from .tile import TerrainEnum, Tile, UnitTypeEnum


def get_ent_tile(target: ActionArgs) -> Tile:
    assert target is not None
    tile = esper.try_component(target, Tile)
    assert tile is not None
    return tile


def get_change_target_tile_action(terrain: TerrainEnum) -> Action:
    def change_target_tile(args: ActionArgs) -> None:
        tile = get_ent_tile(args)
        tile.terrain = terrain
        logger.info(tile.terrain)

    fn = change_target_tile
    return fn


def rotate_target_tile(args: ActionArgs) -> None:
    tile = get_ent_tile(args)
    terrain = TerrainEnum(tile.terrain.value % len(list(TerrainEnum)) + 1)
    get_change_target_tile_action(terrain)(args)


def get_change_target_unit_action(unit: Optional[UnitTypeEnum]) -> Action:
    def change(args: ActionArgs) -> None:
        tile = get_ent_tile(args)
        logger.info(tile.terrain)
        tile.unit = unit

    fn = change
    return fn


def rotate_target_unit(args: ActionArgs) -> None:
    tile = get_ent_tile(args)
    n = tile.unit.value if tile.unit is not None else 0
    n = (n + 1) % (len(list(UnitTypeEnum)) + 1)
    unit = None if n == 0 else UnitTypeEnum(n)
    get_change_target_unit_action(unit)(args)


def switch_unit_types(args: ActionArgs) -> None:
    target_tile = get_ent_tile(args).unit
    ent_tile = get_ent_tile((args)).unit

    get_change_target_unit_action(ent_tile)(args)
    get_change_target_unit_action(target_tile)((args))


def move_ent_unit_to_target_unit(args: ActionArgs) -> None:
    get_ent_tile(args).unit = None
    switch_unit_types(args)


def get_set_target_tile_target_action(pos: Tuple[int, int]) -> Action:
    def set_target_tile_target(ent: ActionArgs) -> None:
        assert ent is not None
        target = MAP_DATA_REF.ent_at(pos)
        get_ent_tile(ent).target = target

    fn = set_target_tile_target
    return fn
