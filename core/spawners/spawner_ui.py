from dataclasses import dataclass
from typing import List, Optional, Tuple

import esper

from common import (
    SETTINGS_REF,
    Action,
    BoundingBox,
    TextFunc,
    TextFuncDecor,
    Untracked,
)
from layer2 import (
    SoundTypeEnum,
    TextData,
    TrackUI,
    UIElementComponent,
    UIElemSprite,
    UIElemType,
    get_sound_action,
)

from .log import logger


@dataclass
class ButtonData:
    size: Tuple[int, int]
    text: str | TextFunc
    ui_elem_type: UIElemType
    click_func: Optional[List[Action]] = None
    click_funcing: Optional[List[Action]] = None
    hover_func: Optional[List[Action]] = None
    start_hover_func: Optional[List[Action]] = None
    remove_hover_func: Optional[List[Action]] = None
    button_default_data: Optional[bool | float] = None


def spawn_button(topleft: Tuple[int, int], data: ButtonData) -> int:
    if SETTINGS_REF.LOG_SPAWNING:
        logger.info("spawning button")
    x, y = topleft
    w, h = data.size
    if not callable(data.text):

        @TextFuncDecor
        def text_func() -> str:
            assert not callable(data.text)
            return data.text

        mod_text = text_func
    else:
        mod_text = data.text

    bb = BoundingBox(
        x,
        x + w * SETTINGS_REF.BUTTON_TILE_SIZE,
        y,
        y + h * SETTINGS_REF.BUTTON_TILE_SIZE,
    )
    offset_x = bb.width / 2
    offset_y = bb.height / 2

    if data.click_func is None:
        data.click_func = []
    if data.click_funcing is None:
        data.click_funcing = []
    if data.hover_func is None:
        data.hover_func = []
    if data.start_hover_func is None:
        data.start_hover_func = []
    if data.remove_hover_func is None:
        data.remove_hover_func = []

    data.click_func.append(get_sound_action(SoundTypeEnum.CLICK))
    data.start_hover_func.append(get_sound_action(SoundTypeEnum.POP))

    if data.ui_elem_type == UIElemType.CHECKBOX:
        offset_x += SETTINGS_REF.BUTTON_TILE_SIZE / 3

    text_data = TextData(mod_text, (offset_x, offset_y))

    clickable: bool = (
        data.ui_elem_type == UIElemType.BUTTON
        or data.ui_elem_type == UIElemType.SLIDER
        or data.ui_elem_type == UIElemType.CHECKBOX
    )
    ui_elem = UIElementComponent(
        text=[text_data],
        click_func=data.click_func,
        clicking_func=data.click_funcing,
        hover_func=data.hover_func,
        start_hover_func=data.start_hover_func,
        end_hover_func=data.remove_hover_func,
        is_clickable=clickable,
        button_val=data.button_default_data,
    )
    tracker = TrackUI()
    ui_elem_sprite = UIElemSprite(data.ui_elem_type, data.size)

    return esper.create_entity(
        bb, ui_elem, tracker, ui_elem_sprite, Untracked()
    )
