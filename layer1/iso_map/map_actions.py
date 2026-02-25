from random import randint
from typing import Optional, Tuple

import esper

from common import SETTINGS_REF, Action, ActionArgs

from .log import logger
from .map import MAP_DATA_REF
from .tile import TerrainEnum, Tile, UnitTypeEnum


def get_ent_tile(ent: ActionArgs) -> Optional[Tile]:
    if ent is None:
        return None
    tile = esper.try_component(ent, Tile)
    if tile is None:
        return None
    return tile


def get_change_target_tile_action(terrain: TerrainEnum) -> Action:
    def change_target_tile(args: ActionArgs) -> None:
        tile = get_ent_tile(args)
        if tile is None:
            return
        tile.terrain = terrain
        logger.info(tile.terrain)

    return change_target_tile


def rotate_target_tile(args: ActionArgs) -> None:
    tile = get_ent_tile(args)
    if tile is None:
        return
    terrain = TerrainEnum(tile.terrain.value % len(list(TerrainEnum)) + 1)
    get_change_target_tile_action(terrain)(args)


def get_change_target_unit_action(unit: Optional[UnitTypeEnum]) -> Action:
    def change(args: ActionArgs) -> None:
        logger.info(f"set unit to {unit}")
        tile = get_ent_tile(args)
        if tile is None:
            return
        tile.unit = unit

    return change


def switch_unit_types(ent: ActionArgs) -> None:
    ent_tile = get_ent_tile(ent)
    if ent_tile is None:
        return

    target = ent_tile.target
    target_tile = get_ent_tile(target)
    if target_tile is None:
        return

    logger.info(f"switch units {ent} - {target}")
    ent_unit = ent_tile.unit
    target_unit = target_tile.unit
    get_change_target_unit_action(ent_unit)(target)
    get_change_target_unit_action(target_unit)(ent)


def get_set_target_tile_target_action(pos: Tuple[int, int]) -> Action:
    def action(ent: ActionArgs) -> None:
        ent_tile = get_ent_tile(ent)
        if ent_tile is None:
            return

        logger.info(f"set target to {pos}")
        target = MAP_DATA_REF.ent_at(pos)
        target_tile = esper.component_for_entity(target, Tile)
        target_tile.is_targeted = True
        ent_tile.target = target

    return action


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


def reset_tile_target(ent: ActionArgs) -> None:
    if ent is None or not esper.has_component(ent, Tile):
        return
    tile = esper.component_for_entity(ent, Tile)
    if tile.target is None:
        return
    target_tile = esper.component_for_entity(tile.target, Tile)
    target_tile.is_targeted = False
    tile.target = None


def transfer_action_to_tile_target(action: Action) -> Action:
    def sub_action(ent: ActionArgs) -> None:
        tile = get_ent_tile(ent)
        if tile is None:
            return
        action(tile.target)

    return sub_action
