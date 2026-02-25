from random import randint
from typing import Optional, Tuple

import esper

from common import SETTINGS_REF, Action, ActionArgs

from .log import logger
from .map import MAP_DATA_REF
from .tile import TerrainEnum, Tile, UnitTypeEnum


def get_ent_tile(ent: ActionArgs) -> Tile:
    assert ent is not None
    tile = esper.try_component(ent, Tile)
    assert tile is not None
    return tile


def get_change_target_tile_action(terrain: TerrainEnum) -> Action:
    def change_target_tile(args: ActionArgs) -> None:
        tile = get_ent_tile(args)
        tile.terrain = terrain
        logger.info(tile.terrain)

    return change_target_tile


def rotate_target_tile(args: ActionArgs) -> None:
    tile = get_ent_tile(args)
    terrain = TerrainEnum(tile.terrain.value % len(list(TerrainEnum)) + 1)
    get_change_target_tile_action(terrain)(args)


def get_change_target_unit_action(unit: Optional[UnitTypeEnum]) -> Action:
    def change(args: ActionArgs) -> None:
        logger.info(f"set unit to {unit}")
        tile = get_ent_tile(args)
        tile.unit = unit

    return change


def switch_unit_types(ent: ActionArgs) -> None:
    ent_tile = get_ent_tile(ent)
    target = ent_tile.target
    target_tile = get_ent_tile(target)

    logger.info(f"switch units {ent} - {target}")
    ent_unit = ent_tile.unit
    target_unit = target_tile.unit
    get_change_target_unit_action(ent_unit)(target)
    get_change_target_unit_action(target_unit)((ent))


def get_set_target_tile_target_action(pos: Tuple[int, int]) -> Action:
    def set_target_tile_target(ent: ActionArgs) -> None:
        logger.info(f"set target to {pos}")
        assert ent is not None
        target = MAP_DATA_REF.ent_at(pos)
        get_ent_tile(ent).target = target

    return set_target_tile_target


def get_spawn_unit_at_random(
    roll_size: int, chance: int, unit: UnitTypeEnum
) -> Action:
    def action(ent: ActionArgs) -> None:
        if randint(0, roll_size) < chance:
            get_change_target_unit_action(unit)(ent)

    return action


def set_random_target(ent: ActionArgs) -> None:
    get_set_target_tile_target_action(
        (
            randint(0, SETTINGS_REF.ISO_MAP_WIDTH - 1),
            randint(0, SETTINGS_REF.ISO_MAP_HEIGHT - 1),
        )
    )(ent)
