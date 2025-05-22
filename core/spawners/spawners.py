from typing import Tuple, Type

import esper

from common import BoundingBox, Health
from layer1.cards import (
    CARD_HEIGHT,
    CARD_START_X,
    CARD_START_Y,
    CARD_WIDTH,
    ROOT_TWO,
    Card,
    select_card,
)
from layer1.iso_map import make_map, map_obj
from layer2 import CardSprite, TrackUI, UIElementComponent
from layer2.ui import click_on_tile

from .log import logger


def spawn_iso_elem(
    offset: Tuple[float, float],
    map_size: Tuple[int, int],
    map_scale: Tuple[int, int],
    map_tracker: Type,
    map_sprite: Type,
    ui_tracker: Type,
) -> int:
    map_obj.tracker_tag = map_tracker
    map_obj.sprite = map_sprite
    map_obj.size = map_size

    left = offset[0]
    right = offset[0] + map_size[0] * map_scale[0] + map_size[1] * map_scale[0]
    top = offset[1] - map_size[1] * map_scale[1] / 2 + map_scale[1]
    bottom = offset[1] + map_size[0] * map_scale[1] * 3 / 2 + map_scale[1]
    ui_bb = BoundingBox(left, right, top, bottom)
    logger.info(f"map ui elem created:{ui_bb.points}")

    ent = esper.create_entity(
        ui_bb, ui_tracker(), UIElementComponent(click_func=click_on_tile)
    )
    make_map()
    return ent


def spawn_card(card: Card) -> int:
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
        UIElementComponent(click_func=select_card),
        Health(),
    )
    return ent
