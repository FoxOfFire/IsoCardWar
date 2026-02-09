import esper
import pygame

from common import (
    POS_PROC_REF,
    Action,
    ActionArgs,
    BoundingBox,
    hover,
    play_card,
    remove_hover,
)

from .audio import SoundTypeEnum, play_sfx
from .ui_utils import get_transformed_mouse_pos, ui_event_obj


def get_sound_action(sound: SoundTypeEnum) -> Action:
    return lambda _: play_sfx(sound)


def click_on_tile(args: ActionArgs) -> None:
    assert args is not None
    ent, _ = args
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
        play_card((intersect, None))


def quit_game(_: ActionArgs = None) -> None:
    pygame.event.post(pygame.event.Event(pygame.QUIT))


def hover_over_tile(args: ActionArgs) -> None:
    assert args is not None
    ent, _ = args
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
        hover((intersect, None))
        return
    remove_hover()
