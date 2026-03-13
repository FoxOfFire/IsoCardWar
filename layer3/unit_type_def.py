from common import (
    SETTINGS_REF,
    ColorEnum,
    PriceEnum,
    get_gain_resource_action,
    reset_trigger,
)
from layer1 import (
    MAP_DATA_REF,
    UnitTypeEnum,
    clear_particles_action,
    get_change_target_unit_action,
    get_spawn_unit_at_random,
    get_target_random_neighbour,
    get_wait_ms_action,
    reset_tile_target,
    transfer_action_to_tile_target,
)

from .actions import get_spawn_dots_between_ent_and_target, random_walk
from .log import logger


def set_type_actions() -> None:
    logger.info("set_type_actions")

    cutoff = SETTINGS_REF.ISO_TARGET_CUTOFF
    red = ColorEnum.RED.value
    MAP_DATA_REF.set_telegraphs_for_type(
        {
            UnitTypeEnum.FARMER: [
                get_wait_ms_action(500),
                reset_trigger,
                get_spawn_dots_between_ent_and_target(cutoff, 0, red),
                get_target_random_neighbour(),
                random_walk(1),
                random_walk(1),
                random_walk(1),
            ],
            UnitTypeEnum.KNIGHT: [
                get_wait_ms_action(500),
                reset_trigger,
                get_spawn_dots_between_ent_and_target(cutoff, 0, red),
                get_target_random_neighbour(),
                random_walk(1),
                random_walk(1),
                random_walk(1),
                random_walk(1),
            ],
        }
    )

    MAP_DATA_REF.set_productions_for_type(
        {
            None: [
                get_wait_ms_action(50),
                get_spawn_unit_at_random(
                    SETTINGS_REF.ISO_SPAWN_CHANCE_MAX,
                    SETTINGS_REF.ISO_FARMER_SPAWN_CHANCE,
                    UnitTypeEnum.FARMER,
                ),
                reset_trigger,
                get_wait_ms_action(50),
                get_spawn_unit_at_random(
                    SETTINGS_REF.ISO_SPAWN_CHANCE_MAX,
                    SETTINGS_REF.ISO_KNIGHT_SPAWN_CHANCE,
                    UnitTypeEnum.KNIGHT,
                ),
            ],
            UnitTypeEnum.CAULDRON: [
                get_gain_resource_action(PriceEnum.BREW, 1),
                get_wait_ms_action(50),
            ],
            UnitTypeEnum.MANA_PYLON: [
                get_gain_resource_action(PriceEnum.MANA, 2),
                get_wait_ms_action(50),
            ],
            UnitTypeEnum.BLOOD_BUCKET: [
                get_gain_resource_action(PriceEnum.BLOOD, 2),
                get_wait_ms_action(50),
            ],
            UnitTypeEnum.WITCH: [
                get_gain_resource_action(PriceEnum.MANA, 5),
                get_wait_ms_action(50),
            ],
            UnitTypeEnum.BIG_CAULDRON: [
                get_gain_resource_action(PriceEnum.BREW, 3),
                get_wait_ms_action(50),
            ],
            UnitTypeEnum.BUSH: [
                get_gain_resource_action(PriceEnum.HERBS, 2),
                get_wait_ms_action(50),
            ],
        }
    )

    MAP_DATA_REF.set_actions_for_type(
        {
            UnitTypeEnum.FARMER: [
                get_wait_ms_action(500),
                reset_trigger,
                reset_tile_target,
                reset_trigger,
                transfer_action_to_tile_target(reset_tile_target),
                clear_particles_action,
                transfer_action_to_tile_target(clear_particles_action),
                reset_trigger,
                transfer_action_to_tile_target(
                    get_change_target_unit_action(None, False)
                ),
            ],
            UnitTypeEnum.KNIGHT: [
                get_wait_ms_action(500),
                reset_trigger,
                reset_tile_target,
                reset_trigger,
                transfer_action_to_tile_target(reset_tile_target),
                reset_trigger,
                transfer_action_to_tile_target(clear_particles_action),
                clear_particles_action,
                reset_trigger,
                transfer_action_to_tile_target(
                    get_change_target_unit_action(None, False)
                ),
            ],
        }
    )
