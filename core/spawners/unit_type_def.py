from random import randint

from common import SETTINGS_REF
from layer1 import (
    MAP_DATA_REF,
    UnitTypeEnum,
    get_change_target_unit_action,
    get_set_target_tile_target_action,
    rotate_target_tile,
    switch_unit_types,
)

from .log import logger


def set_type_actions() -> None:
    logger.info("set_type_actions")

    MAP_DATA_REF.set_actions_for_type(None, [])
    MAP_DATA_REF.set_actions_for_type(
        UnitTypeEnum.CAULDRON,
        [
            get_change_target_unit_action(UnitTypeEnum.BIG_CAULDRON),
        ],
    )
    MAP_DATA_REF.set_actions_for_type(
        UnitTypeEnum.BIG_CAULDRON,
        [
            rotate_target_tile,
        ],
    )
    MAP_DATA_REF.set_actions_for_type(
        UnitTypeEnum.FARMER,
        [
            get_change_target_unit_action(UnitTypeEnum.KNIGHT),
        ],
    )
    MAP_DATA_REF.set_actions_for_type(
        UnitTypeEnum.KNIGHT,
        [
            get_change_target_unit_action(UnitTypeEnum.FARMER),
            get_set_target_tile_target_action(
                (
                    randint(0, SETTINGS_REF.ISO_MAP_WIDTH),
                    randint(0, SETTINGS_REF.ISO_MAP_HEIGHT),
                )
            ),
            switch_unit_types,
        ],
    )
