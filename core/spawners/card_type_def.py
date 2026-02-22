from typing import Callable, Dict

from common import MarkerEnum, PriceEnum
from layer1 import (
    Card,
    CardTypeEnum,
    get_draw_cards_action,
    rotate_target_tile,
    rotate_target_unit,
)
from layer2 import SoundTypeEnum, get_sound_action

CARD_TYPES_DICT_REF: Dict[CardTypeEnum, Callable[[], Card]] = {
    CardTypeEnum.DRAW_ONE: lambda: Card(
        name="Draw",
        description="Draw 3 cards",
        marker=MarkerEnum.ACTION,
        effects=[
            get_draw_cards_action(3),
            get_sound_action(SoundTypeEnum.WHOOSH),
        ],
        price={PriceEnum.MANA: 1, PriceEnum.HERBS: 1, PriceEnum.BLOOD: 1},
    ),
    CardTypeEnum.CHANGE_TERRAIN_AND_DRAW: lambda: Card(
        name="Terraform",
        description="Cycles tile clicked between available",
        marker=MarkerEnum.TERRAIN,
        effects=[
            rotate_target_tile,
            get_sound_action(SoundTypeEnum.TERRAFORM),
        ],
        price={PriceEnum.MANA: 1, PriceEnum.HERBS: 1, PriceEnum.BLOOD: 1},
    ),
    CardTypeEnum.CHANGE_UNIT_AND_DRAW: lambda: Card(
        name="Swap",
        description="Cycles units",
        marker=MarkerEnum.UNIT,
        effects=[rotate_target_unit, get_sound_action(SoundTypeEnum.POP)],
        price={PriceEnum.MANA: 1, PriceEnum.HERBS: 1, PriceEnum.BLOOD: 1},
    ),
}
