from typing import Dict

from common import MarkerEnum, PriceEnum
from layer1 import (
    Card,
    CardTypeEnum,
    change_unit,
    get_draw_cards_action,
    rotate_tiles,
)
from layer2 import SoundTypeEnum, get_sound_action

CARD_TYPES_DICT_REF: Dict[CardTypeEnum, Card] = {
    CardTypeEnum.DRAW_ONE: Card(
        name=CardTypeEnum.DRAW_ONE.value,
        description="Draw 3 cards",
        marker=MarkerEnum.ACTION,
        effects=[
            get_draw_cards_action(3),
            get_sound_action(SoundTypeEnum.WHOOSH),
        ],
        price={PriceEnum.AMMO: 1, PriceEnum.METAL: 1, PriceEnum.FOOD: 1},
    ),
    CardTypeEnum.CHANGE_TERRAIN_AND_DRAW: Card(
        name=CardTypeEnum.CHANGE_TERRAIN_AND_DRAW.value,
        description="Cycles tile clicked between available",
        marker=MarkerEnum.BUILDING,
        effects=[rotate_tiles, get_sound_action(SoundTypeEnum.TERRAFORM)],
        price={PriceEnum.AMMO: 1, PriceEnum.METAL: 1, PriceEnum.FOOD: 1},
    ),
    CardTypeEnum.CHANGE_UNIT_AND_DRAW: Card(
        name=CardTypeEnum.CHANGE_UNIT_AND_DRAW.value,
        description="Cycles units",
        marker=MarkerEnum.UNIT,
        effects=[change_unit, get_sound_action(SoundTypeEnum.POP)],
        price={PriceEnum.AMMO: 1, PriceEnum.METAL: 1, PriceEnum.FOOD: 1},
    ),
}
