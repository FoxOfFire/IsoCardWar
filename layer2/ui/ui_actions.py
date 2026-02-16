from random import random

import esper
import pygame

from common import (
    POS_PROC_REF,
    SETTINGS_REF,
    Action,
    ActionArgs,
    BoundingBox,
    hover,
    play_card,
)
from layer2.tags import GameCameraTag, UIElementComponent

from .audio import SoundTypeEnum, play_sfx
from .ui_utils import (
    get_mouse_pos_in_px,
    get_transformed_mouse_pos,
    ui_event_obj,
)


def get_sound_action(sound: SoundTypeEnum) -> Action:
    return lambda _: play_sfx(sound)


def click_on_tile(ent: ActionArgs) -> None:
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
        play_card(intersect)


def quit_game(_: ActionArgs = None) -> None:
    pygame.event.post(pygame.event.Event(pygame.QUIT))


def flip_ui_elem_val(ent: ActionArgs) -> None:
    assert ent is not None
    ui_elem = esper.try_component(ent, UIElementComponent)
    assert ui_elem is not None
    ui_elem.button_val = not ui_elem.button_val


def toggle_sound(ent: ActionArgs) -> None:
    flip_ui_elem_val(ent)
    assert ent is not None
    ui_elem = esper.try_component(ent, UIElementComponent)
    assert ui_elem is not None
    SETTINGS_REF.GAME_MUTE = ui_elem.button_val


def set_button_val_to_random(ent: ActionArgs) -> None:
    assert ent is not None
    ui_elem = esper.try_component(ent, UIElementComponent)
    assert ui_elem is not None
    ui_elem.button_val = random()


def set_slider_val(ent: ActionArgs) -> None:
    assert ent is not None
    ui_elem = esper.try_component(ent, UIElementComponent)
    bb = esper.try_component(ent, BoundingBox)
    assert ui_elem is not None and bb is not None

    mx, my = get_mouse_pos_in_px()

    t_size = SETTINGS_REF.BUTTON_TILE_SIZE
    if bb.width < t_size + 1:
        w = bb.height - t_size
        t = (my - bb.top - t_size / 2) / w
    else:
        w = bb.width - t_size
        t = (mx - bb.left - t_size / 2) / w

    ui_elem.button_val = min(1.0, max(0.0, t))


def hover_over_tile(ent: ActionArgs) -> None:
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
        hover(intersect)
        return
    hover(None)
