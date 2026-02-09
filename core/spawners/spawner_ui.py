from typing import List, Optional, Tuple

import esper

from common import (
    BUTTON_HEIGHT,
    BUTTON_WIDTH,
    Action,
    BoundingBox,
    TextFunc,
    TextFuncDecor,
    Untracked,
)
from layer2 import (
    TextData,
    TrackUI,
    UIElementComponent,
    UIElemSprite,
    UIElemType,
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

    bb = BoundingBox(x, x + BUTTON_WIDTH, y, y + BUTTON_HEIGHT)
    offset_x = bb.width / 2
    offset_y = bb.height / 2
    text_data = TextData(mod_text, (offset_x, offset_y))

    ui_elem = UIElementComponent(
        text=[text_data],
        click_func=click_func if click_func is not None else [],
        hover_func=hover_func if hover_func is not None else [],
        unhover_func=(
            remove_hover_func if remove_hover_func is not None else []
        ),
    )
    tracker = TrackUI()
    ui_elem_sprite = UIElemSprite(ui_elem_type)

    return esper.create_entity(
        bb, ui_elem, tracker, ui_elem_sprite, Untracked()
    )
