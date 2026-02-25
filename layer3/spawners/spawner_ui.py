from typing import Optional, Tuple

import esper

from common import (
    SETTINGS_REF,
    BoundingBox,
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
from layer3.utils import ButtonData

from .log import logger


def spawn_button(
    topleft: Tuple[int, int],
    data: ButtonData,
    parent: Optional[UIElementComponent] = None,
) -> int:
    if SETTINGS_REF.LOG_SPAWNING:
        logger.info("spawning button")
    x, y = topleft
    assert data.size is not None
    w, h = data.size
    s_w, s_h = data.sub_size
    if w == 1 and s_w != 0:
        s_w = max(SETTINGS_REF.BUTTON_TILE_SIZE // 2, s_w)
    if h == 1 and s_h != 0:
        s_h = max(SETTINGS_REF.BUTTON_TILE_SIZE // 2, s_h)
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
        x + w * SETTINGS_REF.BUTTON_TILE_SIZE + s_w,
        y,
        y + h * SETTINGS_REF.BUTTON_TILE_SIZE + s_h,
    )
    offset_x = bb.width // 2
    offset_y = bb.height // 2

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

    if (
        data.ui_elem_type == UIElemType.CHECKBOX
        or data.ui_elem_type == UIElemType.ICON
    ):
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
        parent_elem=parent,
    )
    tracker = TrackUI()
    ui_elem_sprite = UIElemSprite(
        data.ui_elem_type, data.size, sub_size=data.sub_size
    )

    return esper.create_entity(
        bb, ui_elem, tracker, ui_elem_sprite, Untracked()
    )
