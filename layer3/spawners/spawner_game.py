from functools import partial
from typing import List, Type

import esper

from common import (
    SETTINGS_REF,
    BoundingBox,
    Health,
    Untracked,
    hover,
    play_card,
    select_card,
)
from layer1 import (
    MAP_DATA_REF,
    Card,
    CardTypeEnum,
    ParticleGenerator,
    clear_particles_action,
)
from layer2 import (
    MaskedSprite,
    SoundTypeEnum,
    TextData,
    UIElementComponent,
    get_sound_action,
    get_transfered_to_iso_action,
)
from layer3.actions import get_spawn_dots_between_ent_and_target
from layer3.card_type_def import CARD_TYPES_DICT_REF

from .log import logger


def get_ui_component() -> UIElementComponent:
    return UIElementComponent(
        click_func=[
            get_transfered_to_iso_action(play_card, False, False),
            get_transfered_to_iso_action(clear_particles_action),
            get_transfered_to_iso_action(
                get_spawn_dots_between_ent_and_target(
                    SETTINGS_REF.ISO_TARGET_CUTOFF
                )
            ),
        ],
        click_cancel_func=[
            get_transfered_to_iso_action(clear_particles_action),
            get_transfered_to_iso_action(
                get_spawn_dots_between_ent_and_target(
                    SETTINGS_REF.ISO_TARGET_CUTOFF
                )
            ),
        ],
        hover_func=[
            get_transfered_to_iso_action(
                hover,
            )
        ],
        clicking_func=[
            get_transfered_to_iso_action(
                get_spawn_dots_between_ent_and_target(None)
            ),
        ],
        start_hover_func=[
            get_transfered_to_iso_action(
                get_spawn_dots_between_ent_and_target(
                    SETTINGS_REF.ISO_TARGET_CUTOFF
                )
            ),
        ],
        end_hover_func=[
            hover,
        ],
        text=[],
        is_gameplay_elem=True,
    )


def spawn_iso_elem(map_sprite: Type) -> None:
    map_size = (SETTINGS_REF.ISO_MAP_WIDTH, SETTINGS_REF.ISO_MAP_HEIGHT)
    offset = (SETTINGS_REF.ISO_POS_OFFSET_X, SETTINGS_REF.ISO_POS_OFFSET_Y)
    map_scale = (
        SETTINGS_REF.ISO_TILE_OFFSET_X,
        SETTINGS_REF.ISO_TILE_OFFSET_Y,
    )

    MAP_DATA_REF.set_sprite(map_sprite)
    MAP_DATA_REF.set_particle_generator(ParticleGenerator)

    corrected_offset_y = offset[1] - (map_size[0] - 1) * map_scale[1]

    left = offset[0]
    right = offset[0] + (map_size[0] + map_size[1]) * map_scale[0]
    top = corrected_offset_y
    bottom = corrected_offset_y + (map_size[0] + map_size[1]) * map_scale[1]

    ui_bb = BoundingBox(left, right, top, bottom)

    if SETTINGS_REF.LOG_SPAWNING:
        logger.info(f"map ui elem created:{ui_bb.points}")
    MAP_DATA_REF.make_map(get_ui_component)


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
    for i in range(0, SETTINGS_REF.CARD_PARAGRAPH_LINE_COUNT):
        if len(desc_words) == 0:
            break
        res_str = ""
        while True:
            current_word = desc_words.pop(0)
            if len(res_str) == 0:
                res_str += current_word
            else:
                res_str += " " + current_word
            if (
                len(desc_words) == 0
                or len(res_str + " " + desc_words[-1])
                > SETTINGS_REF.CARD_PARAGRAPH_LETTER_COUNT
            ):
                break

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
        click_cancel_func=[],
        hover_func=[],
        start_hover_func=[hover, get_sound_action(SoundTypeEnum.POP)],
        end_hover_func=[hover],
        text=[text, *description],
        is_gameplay_elem=True,
    )
    # creating card
    ent = esper.create_entity(
        card, bb, MaskedSprite(), ui_elem, Health(), Untracked()
    )
    if SETTINGS_REF.LOG_SPAWNING:
        logger.info(f"created card:{ent}")
    return ent


def create_card_obj(card_type: CardTypeEnum) -> Card:
    return CARD_TYPES_DICT_REF[card_type]()
