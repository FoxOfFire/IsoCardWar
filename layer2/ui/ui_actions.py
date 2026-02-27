from typing import List

import esper
import pygame

from common import (
    POS_PROC_REF,
    SETTINGS_REF,
    STATE_REF,
    Action,
    ActionArgs,
    BoundingBox,
)
from layer2.tags import UIElementComponent

from .audio import SoundTypeEnum, play_sfx
from .ui_utils import get_mouse_pos_in_px


def get_sound_action(sound: SoundTypeEnum) -> Action:
    return lambda _: play_sfx(sound)


def get_transfered_to_iso_actions(
    actions: List[Action],
    act_on_none: bool = True,
    act_on_no_card: bool = True,
) -> Action:
    def sub_action(ent: ActionArgs) -> None:
        for action in actions:
            get_transfered_to_iso_action(action, act_on_none, act_on_no_card)(
                ent
            )

    return sub_action


def get_transfered_to_iso_action(
    action: Action, act_on_none: bool = True, act_on_no_card: bool = True
) -> Action:
    def sub_action(ent: ActionArgs) -> None:
        if STATE_REF.selected_card is None and not act_on_no_card:
            return
        assert ent is not None
        mouse_x, mouse_y = get_mouse_pos_in_px()
        mouse_bb = BoundingBox(mouse_x, mouse_x, mouse_y, mouse_y)

        for intersect in POS_PROC_REF().intersect(mouse_bb):
            action(intersect)
            return
        if act_on_none:
            action(None)

    return sub_action


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
    assert ui_elem is not None and isinstance(ui_elem.button_val, bool)
    SETTINGS_REF.GAME_MUTE = ui_elem.button_val


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
