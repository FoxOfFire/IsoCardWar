from typing import Optional, Tuple

import esper

from common import BoundingBox, Untracked
from common.constants import BUTTON_HEIGHT, BUTTON_WIDTH
from common.types import ButtonFunc, TextFunc
from layer2 import TextData, TrackUI, UIElementComponent
from layer2.rendering import UIElemSprite, UIElemType

from .log import logger


def spawn_button(
    topleft: Tuple[float, float],
    text: str | TextFunc,
    ui_elem_type: UIElemType,
    /,
    *,
    click_func: Optional[ButtonFunc] = None,
    hover_func: Optional[ButtonFunc] = None,
    remove_hover_func: Optional[ButtonFunc] = None,
) -> int:
    logger.info("spawning button")
    x, y = topleft
    if not callable(text):

        def text_func() -> str:
            if callable(text):
                raise RuntimeError("text somehow callable and not callable")
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
        click_func=click_func,
        hover_func=hover_func,
        unhover_func=remove_hover_func,
    )
    tracker = TrackUI()
    ui_elem_sprite = UIElemSprite(ui_elem_type)

    return esper.create_entity(
        bb, ui_elem, tracker, ui_elem_sprite, Untracked()
    )
