from common import SETTINGS_REF, PriceEnum, get_gain_resource_action
from layer1 import (
    MAP_DATA_REF,
    UnitTypeEnum,
    get_spawn_unit_at_random,
    get_wait_ms_action,
    set_random_target,
    switch_unit_types,
)

from .log import logger


def set_type_actions() -> None:
    logger.info("set_type_actions")

    MAP_DATA_REF.set_actions_for_type(
        None,
        [
            get_spawn_unit_at_random(
                SETTINGS_REF.ISO_SPAWN_CHANCE_MAX,
                SETTINGS_REF.ISO_FARMER_SPAWN_CHANCE,
                UnitTypeEnum.FARMER,
            ),
            get_spawn_unit_at_random(
                SETTINGS_REF.ISO_SPAWN_CHANCE_MAX,
                SETTINGS_REF.ISO_KNIGHT_SPAWN_CHANCE,
                UnitTypeEnum.KNIGHT,
            ),
        ],
    )
    MAP_DATA_REF.set_actions_for_type(
        UnitTypeEnum.CAULDRON,
        [
            get_gain_resource_action(PriceEnum.BREW, 1),
        ],
    )
    MAP_DATA_REF.set_actions_for_type(
        UnitTypeEnum.MANA_PYLON,
        [
            get_gain_resource_action(PriceEnum.MANA, 2),
        ],
    )
    MAP_DATA_REF.set_actions_for_type(
        UnitTypeEnum.BLOOD_BUCKET,
        [
            get_gain_resource_action(PriceEnum.BLOOD, 2),
        ],
    )
    MAP_DATA_REF.set_actions_for_type(
        UnitTypeEnum.WITCH,
        [
            get_gain_resource_action(PriceEnum.MANA, 5),
        ],
    )
    MAP_DATA_REF.set_actions_for_type(
        UnitTypeEnum.BIG_CAULDRON,
        [
            get_gain_resource_action(PriceEnum.BREW, 3),
        ],
    )
    MAP_DATA_REF.set_actions_for_type(
        UnitTypeEnum.BUSH,
        [
            get_gain_resource_action(PriceEnum.HERBS, 2),
        ],
    )
    MAP_DATA_REF.set_actions_for_type(
        UnitTypeEnum.FARMER,
        [
            switch_unit_types,
            set_random_target,
            get_wait_ms_action(100),
        ],
    )
    MAP_DATA_REF.set_actions_for_type(
        UnitTypeEnum.KNIGHT,
        [
            switch_unit_types,
            set_random_target,
            get_wait_ms_action(100),
        ],
    )
