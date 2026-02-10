from typing import Optional

import esper

from common import Action, ActionArgs, flip_action_args

from .log import logger
from .tile import TerrainEnum, Tile, UnitTypeEnum


def get_target_tile(args: ActionArgs) -> Tile:
    assert args is not None
    _, target = args
    assert target is not None
    tile = esper.try_component(target, Tile)
    assert tile is not None
    return tile


def get_change_tile_to_action(terrain: TerrainEnum) -> Action:
    def change(args: ActionArgs) -> None:
        tile = get_target_tile(args)
        tile.terrain = terrain
        logger.info(tile.terrain)

    fn = change
    return fn


def rotate_tiles(args: ActionArgs) -> None:
    tile = get_target_tile(args)
    terrain = TerrainEnum(tile.terrain.value % len(list(TerrainEnum)) + 1)
    get_change_tile_to_action(terrain)(args)


def get_change_unit_action(unit: Optional[UnitTypeEnum]) -> Action:
    def change(args: ActionArgs) -> None:
        tile = get_target_tile(args)
        logger.info(tile.terrain)
        tile.unit = unit

    fn = change
    return fn


def change_unit(args: ActionArgs) -> None:
    tile = get_target_tile(args)
    n = tile.unit.value if tile.unit is not None else 0
    n = (n + 1) % (len(list(UnitTypeEnum)) + 1)
    unit = None if n == 0 else UnitTypeEnum(n)
    get_change_unit_action(unit)(args)


def switch_unit_types(args: ActionArgs) -> None:
    target_tile = get_target_tile(args).unit
    ent_tile = get_target_tile(flip_action_args(args)).unit

    get_change_unit_action(ent_tile)(args)
    get_change_unit_action(target_tile)(flip_action_args(args))


def move_unit_to(args: ActionArgs) -> None:
    get_target_tile(args).unit = None
    switch_unit_types(args)
