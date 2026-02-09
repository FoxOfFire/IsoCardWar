from typing import Optional

import esper
import pygame

from common import (
    POS_PROC_REF,
    ActionDecor,
    BoundingBox,
    hover,
    play_card,
    remove_hover,
)

from .ui_utils import get_transformed_mouse_pos, ui_event_obj


@ActionDecor
def click_on_tile(ent: Optional[int], _: Optional[int]) -> None:
    assert ent is not None
    bb = esper.component_for_entity(ent, BoundingBox)
    trans_mouse_pos = get_transformed_mouse_pos(bb)
    mouse_bb = BoundingBox(
        trans_mouse_pos[0],
        trans_mouse_pos[0],
        trans_mouse_pos[1],
        trans_mouse_pos[1],
    )
    assert ui_event_obj.iso_tag is not None

    for intersect in POS_PROC_REF.intersect(mouse_bb, ui_event_obj.iso_tag):
        play_card(intersect, None)


@ActionDecor
def quit_game(_: Optional[int], __: Optional[int]) -> None:
    pygame.event.post(pygame.event.Event(pygame.QUIT))


@ActionDecor
def hover_over_tile(ent: Optional[int], _: Optional[int]) -> None:
    assert ent is not None
    bb = esper.component_for_entity(ent, BoundingBox)
    trans_mouse_pos = get_transformed_mouse_pos(bb)
    mouse_bb = BoundingBox(
        trans_mouse_pos[0],
        trans_mouse_pos[0],
        trans_mouse_pos[1],
        trans_mouse_pos[1],
    )
    assert ui_event_obj.iso_tag is not None

    for intersect in POS_PROC_REF.intersect(mouse_bb, ui_event_obj.iso_tag):
        hover(intersect, None)
        return
    remove_hover(None, None)
