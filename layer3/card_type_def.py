from typing import Callable, Dict

from common import PriceEnum, get_gain_resource_action
from layer1 import (
    Card,
    CardTypeEnum,
    UnitTypeEnum,
    get_change_target_unit_action,
    get_draw_cards_action,
    rotate_target_tile,
)
from layer2 import SoundTypeEnum, get_sound_action

CARD_TYPES_DICT_REF: Dict[CardTypeEnum, Callable[[], Card]] = {
    CardTypeEnum.DRAW: lambda: Card(
        name="Draw",
        description="Draw 3 cards",
        effects=[
            get_draw_cards_action(3),
            get_sound_action(SoundTypeEnum.WHOOSH),
        ],
        price={
            PriceEnum.MANA: 1,
            PriceEnum.HERBS: 1,
            PriceEnum.BLOOD: 0,
            PriceEnum.BREW: 2,
        },
    ),
    CardTypeEnum.MANA_PYLON: lambda: Card(
        name="Mana Pylon",
        description="Spawns a mana pylon",
        effects=[
            get_change_target_unit_action(UnitTypeEnum.MANA_PYLON),
            get_sound_action(SoundTypeEnum.POP),
        ],
        price={
            PriceEnum.MANA: 1,
            PriceEnum.HERBS: 0,
            PriceEnum.BLOOD: 1,
            PriceEnum.BREW: 1,
        },
    ),
    CardTypeEnum.BLOOD_BUCKET: lambda: Card(
        name="Blood Bucket",
        description="Spawns a blood bucket",
        effects=[
            get_change_target_unit_action(UnitTypeEnum.BLOOD_BUCKET),
            get_sound_action(SoundTypeEnum.POP),
        ],
        price={
            PriceEnum.MANA: 0,
            PriceEnum.HERBS: 1,
            PriceEnum.BLOOD: 2,
            PriceEnum.BREW: 1,
        },
    ),
    CardTypeEnum.CHANGE_TERRAIN: lambda: Card(
        name="Terraform",
        description="Cycles tile clicked between available",
        effects=[
            rotate_target_tile,
            get_sound_action(SoundTypeEnum.TERRAFORM),
        ],
        price={
            PriceEnum.MANA: 0,
            PriceEnum.HERBS: 1,
            PriceEnum.BLOOD: 1,
            PriceEnum.BREW: 2,
        },
    ),
    CardTypeEnum.BUSH: lambda: Card(
        name="Berry Bush",
        description="Spawns a Berry Bush",
        effects=[
            get_change_target_unit_action(UnitTypeEnum.BUSH),
            get_sound_action(SoundTypeEnum.POP),
        ],
        price={
            PriceEnum.MANA: 2,
            PriceEnum.HERBS: 0,
            PriceEnum.BLOOD: 1,
            PriceEnum.BREW: 0,
        },
    ),
    CardTypeEnum.CAULDRON: lambda: Card(
        name="Cauldron",
        description="Spawns a cauldron",
        effects=[
            get_change_target_unit_action(UnitTypeEnum.CAULDRON),
            get_sound_action(SoundTypeEnum.POP),
        ],
        price={
            PriceEnum.MANA: 1,
            PriceEnum.HERBS: 1,
            PriceEnum.BLOOD: 0,
            PriceEnum.BREW: 0,
        },
    ),
    CardTypeEnum.BIG_CAULDRON: lambda: Card(
        name="Big Cauldron",
        description="Spawns a big cauldron",
        effects=[
            get_change_target_unit_action(UnitTypeEnum.BIG_CAULDRON),
            get_sound_action(SoundTypeEnum.POP),
        ],
        price={
            PriceEnum.MANA: 1,
            PriceEnum.HERBS: 1,
            PriceEnum.BLOOD: 2,
            PriceEnum.BREW: 2,
        },
    ),
    CardTypeEnum.REMOVE_UNIT: lambda: Card(
        name="Remove unit",
        description="Removes target unit",
        effects=[
            get_change_target_unit_action(None),
            get_gain_resource_action(PriceEnum.BLOOD, 2),
            get_sound_action(SoundTypeEnum.POP),
        ],
        price={
            PriceEnum.MANA: 1,
            PriceEnum.HERBS: 0,
            PriceEnum.BLOOD: 0,
            PriceEnum.BREW: 2,
        },
    ),
}
