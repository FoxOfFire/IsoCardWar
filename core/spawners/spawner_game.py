from functools import partial
from random import randint
from typing import List, Type

import esper

from common import BoundingBox, Health
from common.constants import (
    CARD_HEIGHT,
    CARD_PARAGRAPH_LETTER_COUNT,
    CARD_PARAGRAPH_LINE_COUNT,
    CARD_PARAGRAPH_TEXT_RELATIVE_Y_OFFSET,
    CARD_PARAGRAPH_TEXT_RELATIVE_Y_ONE,
    CARD_START_X,
    CARD_START_Y,
    CARD_TEXT_RELATIVE_POS_X,
    CARD_TITLE_TEXT_RELATIVE_POS_Y,
    CARD_WIDTH,
    ISO_MAP_HEIGHT,
    ISO_MAP_WIDTH,
    ISO_POS_OFFSET_X,
    ISO_POS_OFFSET_Y,
    ISO_TILE_OFFSET_X,
    ISO_TILE_OFFSET_Y,
)
from layer1 import MarkerEnum, PriceEnum, hover, remove_hover, select
from layer1.cards import Card, CardTypeEnum, draw_cards
from layer1.iso_map import change_tile, change_unit, make_map, map_obj
from layer2 import TextData, TrackUI, UIElementComponent
from layer2.rendering import CardSprite
from layer2.ui import click_on_tile, hover_over_tile

from .log import logger


def spawn_iso_elem(
    map_tracker: Type,
    ui_tracker: Type,
    map_sprite: Type,
    /,
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
        corrected_offset_y + map_size[0] *
        map_scale[1] + map_size[1] * map_scale[1]
    )
    ui_bb = BoundingBox(left, right, top, bottom)
    logger.info(f"map ui elem created:{ui_bb.points}")

    ent = esper.create_entity(
        ui_bb,
        ui_tracker(),
        UIElementComponent(
            click_func=click_on_tile,
            hover_func=hover_over_tile,
            unhover_func=remove_hover,
            is_gameplay_elem=True,
        ),
    )
    make_map()
    return ent


def spawn_card_ent(card: Card, /) -> int:
    """
    #creates card entity

    does not add to deck
    """

    bb = BoundingBox(
        CARD_START_X,
        CARD_START_X + CARD_WIDTH,
        CARD_START_Y,
        CARD_START_Y + CARD_HEIGHT,
    )
    text = TextData(
        lambda: card.name,
        (CARD_TEXT_RELATIVE_POS_X, CARD_TITLE_TEXT_RELATIVE_POS_Y),
    )

    description: List[TextData] = []
    desc_words = card.description.split()
    assert len(desc_words) > 0, "No card description given"
    current_word: str = desc_words.pop(0)
    for i in range(0, CARD_PARAGRAPH_LINE_COUNT):
        if len(desc_words) == 0:
            break
        res_str = ""
        while True:
            if len(res_str + " " + current_word) > CARD_PARAGRAPH_LETTER_COUNT:
                break
            res_str += " " + current_word
            if len(desc_words) == 0:
                break
            current_word = desc_words.pop(0)

        def decr_text_func(res_str: str) -> str:
            return res_str

        description.append(
            TextData(
                partial(decr_text_func, res_str),
                (
                    CARD_TEXT_RELATIVE_POS_X - 1,
                    CARD_PARAGRAPH_TEXT_RELATIVE_Y_ONE
                    + i * CARD_PARAGRAPH_TEXT_RELATIVE_Y_OFFSET,
                ),
            )
        )

    ui_elem = UIElementComponent(
        click_func=select,
        hover_func=hover,
        unhover_func=remove_hover,
        text=[text, *description],
        is_gameplay_elem=True,
    )
    # creating card
    ent = esper.create_entity(
        card, bb, TrackUI(), CardSprite(), ui_elem, Health())
    return ent


def create_card_obj(card_type: CardTypeEnum) -> Card:
    rand = randint(2, 4)
    match card_type:
        case CardTypeEnum.DRAW_ONE:
            marker = MarkerEnum.ACTION
            effects = draw_cards(rand)
            description = f"Draw {rand} card" + ("s" if rand > 1 else "")
        case CardTypeEnum.CHANGE_TERRAIN_AND_DRAW:
            marker = MarkerEnum.BUILDING
            effects = change_tile()
            description = "Cycles tile clicked between available"
        case CardTypeEnum.CHANGE_UNIT_AND_DRAW:
            marker = MarkerEnum.UNIT
            effects = change_unit()
            description = "Cycles units"
        case _:
            raise RuntimeError("unexpected card type")

    prices = {PriceEnum.AMMO: 1, PriceEnum.METAL: 1, PriceEnum.FOOD: 1}
    return Card(f"{card_type.value}", description, prices, marker, effects)
