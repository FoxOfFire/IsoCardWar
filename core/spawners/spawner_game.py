from functools import partial
from typing import List, Type

import esper

from common import (
    SETTINGS_REF,
    BoundingBox,
    Health,
    Untracked,
    hover,
    select_card,
)
from layer1 import MAP_DATA_REF, Card, CardTypeEnum
from layer2 import (
    CardSprite,
    SoundTypeEnum,
    TextData,
    TrackUI,
    UIElementComponent,
    click_on_tile,
    get_sound_action,
    hover_over_tile,
)

from .card_type_def import CARD_TYPES_DICT_REF
from .log import logger


def spawn_iso_elem(
    map_tracker: Type,
    ui_tracker: Type,
    map_sprite: Type,
    /,
) -> int:
    map_size = (SETTINGS_REF.ISO_MAP_WIDTH, SETTINGS_REF.ISO_MAP_HEIGHT)
    offset = (SETTINGS_REF.ISO_POS_OFFSET_X, SETTINGS_REF.ISO_POS_OFFSET_Y)
    map_scale = (
        SETTINGS_REF.ISO_TILE_OFFSET_X,
        SETTINGS_REF.ISO_TILE_OFFSET_Y,
    )

    MAP_DATA_REF.tracker_tag = map_tracker
    MAP_DATA_REF.sprite = map_sprite

    corrected_offset_y = offset[1] - (map_size[0] - 1) * map_scale[1]

    left = offset[0]
    right = offset[0] + (map_size[0] + map_size[1]) * map_scale[0]
    top = corrected_offset_y
    bottom = corrected_offset_y + (map_size[0] + map_size[1]) * map_scale[1]

    ui_bb = BoundingBox(left, right, top, bottom)
    logger.info(f"map ui elem created:{ui_bb.points}")

    ent = esper.create_entity(
        ui_bb,
        ui_tracker(),
        UIElementComponent(
            click_func=[click_on_tile],
            hover_func=[hover_over_tile],
            clicking_func=[],
            start_hover_func=[],
            end_hover_func=[hover],
            text=[],
            is_gameplay_elem=True,
        ),
        Untracked(),
    )
    MAP_DATA_REF.make_map()
    return ent


def spawn_card_ent(card: Card, /) -> int:
    """
    #creates card entity

    does not add to deck
    """

    bb = BoundingBox(
        SETTINGS_REF.CARD_START_X,
        SETTINGS_REF.CARD_START_X + SETTINGS_REF.CARD_WIDTH,
        SETTINGS_REF.CARD_START_Y,
        SETTINGS_REF.CARD_START_Y + SETTINGS_REF.CARD_HEIGHT,
    )
    text = TextData(
        lambda: card.name,
        (
            SETTINGS_REF.CARD_TEXT_RELATIVE_POS_X,
            SETTINGS_REF.CARD_TITLE_TEXT_RELATIVE_POS_Y,
        ),
    )

    description: List[TextData] = []
    desc_words = card.description.split()
    assert len(desc_words) > 0, "No card description given"
    current_word: str = desc_words.pop(0)
    for i in range(0, SETTINGS_REF.CARD_PARAGRAPH_LINE_COUNT):
        if len(desc_words) == 0:
            break
        res_str = ""
        while True:
            if (
                len(res_str + " " + current_word)
                > SETTINGS_REF.CARD_PARAGRAPH_LETTER_COUNT
            ):
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
                    SETTINGS_REF.CARD_TEXT_RELATIVE_POS_X - 1,
                    SETTINGS_REF.CARD_PARAGRAPH_TEXT_RELATIVE_Y_ONE
                    + i * SETTINGS_REF.CARD_PARAGRAPH_TEXT_RELATIVE_Y_OFFSET,
                ),
            )
        )

    ui_elem = UIElementComponent(
        click_func=[select_card, get_sound_action(SoundTypeEnum.CLICK)],
        clicking_func=[],
        hover_func=[],
        start_hover_func=[hover, get_sound_action(SoundTypeEnum.POP)],
        end_hover_func=[hover],
        text=[text, *description],
        is_gameplay_elem=True,
    )
    # creating card
    ent = esper.create_entity(
        card, bb, TrackUI(), CardSprite(), ui_elem, Health(), Untracked()
    )
    logger.info(f"created card:{ent}")
    return ent


def create_card_obj(card_type: CardTypeEnum) -> Card:
    return CARD_TYPES_DICT_REF[card_type]
