from layer1 import (
    MAP_DATA_REF,
    UnitTypeEnum,
    get_change_target_unit_action,
    rotate_target_tile,
    set_random_target,
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
            switch_unit_types,
            set_random_target,
        ],
    )
