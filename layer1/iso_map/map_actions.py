from random import randint
from typing import Optional, Tuple

import esper

from common import (
    SETTINGS_REF,
    STATE_REF,
    Action,
    ActionDecor,
    ActionEnt,
    select_tile,
    shuffle_list,
)

from .log import logger
from .map import MAP_DATA_REF
from .tile import TerrainEnum, Tile, UnitTypeEnum


def get_ent_tile(ent: ActionEnt) -> Optional[Tile]:
    if ent is None:
        return None
    tile = esper.try_component(ent, Tile)
    if tile is None:
        return None
    return tile


def get_change_target_tile_action(terrain: TerrainEnum) -> Action:
    @ActionDecor
    def change_target_tile(args: ActionEnt) -> bool:
        tile = get_ent_tile(args)
        if tile is None:
            return False
        tile.terrain = terrain
        if SETTINGS_REF.LOG_MAP_ACTIONS:
            logger.info(tile.terrain)
        return True

    return change_target_tile


@ActionDecor
def rotate_target_tile(args: ActionEnt) -> bool:
    tile = get_ent_tile(args)
    if tile is None:
        return False
    terrain = TerrainEnum(tile.terrain.value % len(list(TerrainEnum)) + 1)
    return get_change_target_tile_action(terrain)(args, True)


def get_change_target_unit_action(
    unit: Optional[UnitTypeEnum], modify_empty_only: bool
) -> Action:
    @ActionDecor
    def change(args: ActionEnt) -> bool:
        if SETTINGS_REF.LOG_MAP_ACTIONS:
            logger.info(f"set unit to {unit}")
        tile = get_ent_tile(args)
        if tile is None:
            return False
        if modify_empty_only and tile.unit is not None:
            return False
        if tile.unit == unit:
            return False
        if tile.target is not None:
            target = get_ent_tile(tile.target)
            if target is not None:
                target.is_targeted = max(0, target.is_targeted - 1)
                tile.target = None
        tile.unit = unit
        return True

    return change


@ActionDecor
def switch_unit_types(ent: ActionEnt) -> bool:
    ent_tile = get_ent_tile(ent)
    if ent_tile is None:
        return False

    target = ent_tile.target
    target_tile = get_ent_tile(target)
    if target_tile is None:
        return False

    if SETTINGS_REF.LOG_MAP_ACTIONS:
        logger.info(f"switch units {ent} - {target}")
    ent_unit = ent_tile.unit
    target_unit = target_tile.unit
    if not get_change_target_unit_action(ent_unit, False)(target, True):
        return False
    if not get_change_target_unit_action(target_unit, False)(ent, True):
        get_change_target_unit_action(target_unit, False)(target, True)
        return False
    return True


def get_set_target_tile_target_action(pos: Tuple[int, int]) -> Action:
    @ActionDecor
    def action(ent: ActionEnt) -> bool:
        x, y = pos
        if (x < 0 or x >= SETTINGS_REF.ISO_MAP_WIDTH) or (
            y < 0 or y >= SETTINGS_REF.ISO_MAP_HEIGHT
        ):
            return False
        ent_tile = get_ent_tile(ent)
        if ent_tile is None:
            return False

        if SETTINGS_REF.LOG_MAP_ACTIONS:
            logger.info(f"set target to {pos}")
        target = MAP_DATA_REF.ent_at(pos)
        target_tile = esper.component_for_entity(target, Tile)
        target_tile.is_targeted += 1
        ent_tile.target = target
        return True

    return action


def get_set_target_tile_relative_target_action(pos: Tuple[int, int]) -> Action:
    @ActionDecor
    def action(ent: ActionEnt) -> bool:
        if ent is None:
            return False
        x, y = MAP_DATA_REF.pos_at(ent)
        dx, dy = pos
        if get_set_target_tile_target_action((x + dx, y + dy))(ent, True):
            return True
        if MAP_DATA_REF.valid_ent_pos((x + dx, y + dy)):
            reset_tile_target(MAP_DATA_REF.ent_at((x + dx, y + dy)), True)
        reset_tile_target(MAP_DATA_REF.ent_at((x, y)), True)
        return False

    return action


def get_spawn_unit_at_random(
    roll_size: int, chance: int, unit: UnitTypeEnum
) -> Action:
    @ActionDecor
    def action(ent: ActionEnt) -> bool:
        tile = get_ent_tile(ent)
        if tile is None or tile.terrain == TerrainEnum.WATER:
            return False
        if randint(0, roll_size) < chance:
            return get_change_target_unit_action(unit, True)(ent, True)
        return False

    return action


@ActionDecor
def set_random_target(ent: ActionEnt) -> bool:
    success = get_set_target_tile_target_action(
        (
            randint(0, SETTINGS_REF.ISO_MAP_WIDTH - 1),
            randint(0, SETTINGS_REF.ISO_MAP_HEIGHT - 1),
        )
    )(ent, True)
    if not success:
        return False
    tile = get_ent_tile(ent)
    assert tile is not None
    target_tile = get_ent_tile(tile.target)
    assert target_tile is not None
    if target_tile.terrain != TerrainEnum.WATER:
        return True
    reset_tile_target(ent, True)

    return False


@ActionDecor
def reset_tile_target(ent: ActionEnt) -> bool:
    if ent is None or not esper.has_component(ent, Tile):
        return False
    tile = esper.component_for_entity(ent, Tile)
    if tile.target is None:
        return True
    target_tile = esper.component_for_entity(tile.target, Tile)
    target_tile.is_targeted = max(0, target_tile.is_targeted - 1)
    tile.target = None
    return True


def transfer_action_to_tile_target(action: Action) -> Action:
    @ActionDecor
    def sub_action(ent: ActionEnt) -> bool:
        tile = get_ent_tile(ent)
        if tile is None:
            return False
        return action(tile.target, True)

    return sub_action


@ActionDecor
def set_active_tile(ent: ActionEnt) -> bool:
    STATE_REF.active_tile = ent
    return True


@ActionDecor
def reset_active_tile(ent: ActionEnt) -> bool:
    return set_active_tile(None, True)


def get_move_realtive_action(pos: Tuple[int, int]) -> Action:
    @ActionDecor
    def action(ent: ActionEnt) -> bool:
        if not get_set_target_tile_relative_target_action(pos)(ent, True):
            return False

        tile = get_ent_tile(ent)
        assert tile is not None
        target_ent = tile.target
        target_tile = get_ent_tile(target_ent)

        if (
            target_tile is None
            or target_tile.terrain == TerrainEnum.WATER
            or target_tile.unit is not None
            or not switch_unit_types(ent, True)
        ):
            reset_tile_target(ent, True)
            return False
        reset_tile_target(ent, True)

        set_active_tile(target_ent, True)

        return select_tile(target_ent, True)

    return action


def get_target_random_neighbour() -> Action:
    @ActionDecor
    def action(ent: ActionEnt) -> bool:
        tile = get_ent_tile(ent)
        if tile is None:
            return False
        if not reset_tile_target(ent, True) or ent is None:
            return False
        dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        dirs = shuffle_list(dirs)
        for i in range(4):
            if get_set_target_tile_relative_target_action(dirs[i])(ent, True):
                if tile.target is None:
                    continue
                target_tile = get_ent_tile(tile.target)
                if target_tile is None:
                    continue
                if (
                    target_tile.unit is not None
                    and target_tile.unit != UnitTypeEnum.WITCH
                ):
                    break

            reset_tile_target(ent, True)

        return True

    return action
