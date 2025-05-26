from random import randint
from typing import Type

import esper

from common import BoundingBox, Health
from common.constants import (
    CARD_HEIGHT,
    CARD_START_X,
    CARD_START_Y,
    CARD_WIDTH,
    ISO_MAP_HEIGHT,
    ISO_MAP_WIDTH,
    ISO_POS_OFFSET_X,
    ISO_POS_OFFSET_Y,
    ISO_TILE_OFFSET_X,
    ISO_TILE_OFFSET_Y,
    ROOT_TWO,
)
from layer1 import MarkerEnum, PriceEnum
from layer1.cards import (
    Card,
    CardTypeEnum,
    draw_cards,
    hover_over_card,
    remove_hover_over_card,
    select_card,
)
from layer1.iso_map import (
    TerrainEnum,
    make_map,
    map_obj,
    rotate_between_tiles,
    rotate_between_units,
)
from layer2 import CardSprite, TrackUI, UIElementComponent
from layer2.ui import click_on_tile

from .log import logger


def spawn_iso_elem(
    map_tracker: Type,
    map_sprite: Type,
    ui_tracker: Type,
) -> int:
    map_size = (ISO_MAP_WIDTH, ISO_MAP_HEIGHT)
    offset = (ISO_POS_OFFSET_X, ISO_POS_OFFSET_Y)
    map_scale = (ISO_TILE_OFFSET_X, ISO_TILE_OFFSET_Y)

    map_obj.tracker_tag = map_tracker
    map_obj.sprite = map_sprite
    map_obj.size = map_size

    corrected_offset_y = offset[1] - (map_size[0] - 1) * map_scale[1]

    left = offset[0]
    right = offset[0] + (map_size[0] + map_size[1]) * map_scale[0]
    top = corrected_offset_y
    bottom = (
        corrected_offset_y + map_size[0] * map_scale[1] + map_size[1] * map_scale[1]
    )
    ui_bb = BoundingBox(left, right, top, bottom)
    logger.info(f"map ui elem created:{ui_bb.points}")

    ent = esper.create_entity(
        ui_bb, ui_tracker(), UIElementComponent(click_func=click_on_tile)
    )
    make_map()
    return ent


def spawn_card_ent(card: Card) -> int:
    """
    #creates card entity

    does not add to deck
    """
    # calculating bb size
    bb_size = ROOT_TWO / 2 * (CARD_HEIGHT + CARD_WIDTH)

    width_offset = (bb_size - CARD_WIDTH) / 2
    height_offset = (bb_size - CARD_HEIGHT) / 2

    bb = BoundingBox(
        CARD_START_X - width_offset,
        CARD_START_X + width_offset + CARD_WIDTH,
        CARD_START_Y - height_offset,
        CARD_START_Y + height_offset + CARD_HEIGHT,
    )

    # creating card
    card.current_angle = 0
    card.target_angle = None
    ent = esper.create_entity(
        card,
        bb,
        TrackUI(),
        CardSprite(),
        UIElementComponent(
            click_func=select_card,
            hover_func=hover_over_card,
            unhover_func=remove_hover_over_card,
        ),
        Health(),
    )
    return ent


def create_card_obj(card_type: CardTypeEnum) -> Card:
    def noop(ent: int, target: int) -> None:
        logger.info(f"noop({ent}, {target})")

    match card_type:
        case CardTypeEnum.DRAW_TWO:
            marker = MarkerEnum.ACTION
            effects = draw_cards(3)
        case CardTypeEnum.TURN_TO_CONCRETE:
            marker = MarkerEnum.BUILDING
            effects = rotate_between_tiles()
        case CardTypeEnum.TURN_TO_GRASS:
            marker = MarkerEnum.UNIT
            effects = rotate_between_units()
        case _:
            marker = MarkerEnum.UNIQUE
            effects = [noop]

    return Card(
        f"Dummy {randint(1, 1000)}",
        {PriceEnum.AMMO: 1, PriceEnum.METAL: 1, PriceEnum.FOOD: 1},
        marker,
        effects,
        0,
        20,
    )
