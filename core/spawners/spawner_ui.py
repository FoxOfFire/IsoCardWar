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


def spawn_button(
    topleft: Tuple[float, float],
    text: str | TextFunc,
    ui_elem_type: UIElemType,
    /,
    *,
    click_func: Optional[List[Action]] = None,
    hover_func: Optional[List[Action]] = None,
    start_hover_func: Optional[List[Action]] = None,
    remove_hover_func: Optional[List[Action]] = None,
) -> int:
    logger.info("spawning button")
    x, y = topleft
    if not callable(text):

        @TextFuncDecor
        def text_func() -> str:
            assert not callable(text)
            return text

        mod_text = text_func
    else:
        mod_text = text

    bb = BoundingBox(
        x, x + SETTINGS_REF.BUTTON_WIDTH, y, y + SETTINGS_REF.BUTTON_HEIGHT
    )
    offset_x = bb.width / 2
    offset_y = bb.height / 2
    text_data = TextData(mod_text, (offset_x, offset_y))

    if click_func is None:
        click_func = []
    if hover_func is None:
        hover_func = []
    if start_hover_func is None:
        start_hover_func = []
    if remove_hover_func is None:
        remove_hover_func = []
    click_func.append(get_sound_action(SoundTypeEnum.CLICK))
    start_hover_func.append(get_sound_action(SoundTypeEnum.POP))

    ui_elem = UIElementComponent(
        text=[text_data],
        click_func=click_func,
        hover_func=hover_func,
        start_hover_func=start_hover_func,
        end_hover_func=remove_hover_func,
    )
    tracker = TrackUI()
    ui_elem_sprite = UIElemSprite(ui_elem_type)

    return esper.create_entity(
        bb, ui_elem, tracker, ui_elem_sprite, Untracked()
    )
