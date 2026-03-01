import esper
import pygame

from common import (
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


def card_guard(action: Action) -> Action:
    def sub_acton(ent: ActionArgs) -> None:
        if STATE_REF.selected_card is not None and ent is not None:
            action(ent)

    return sub_acton


def quit_game(_: ActionArgs = None) -> None:
    pygame.event.post(pygame.event.Event(pygame.QUIT))


def flip_ui_elem_val(ent: ActionArgs) -> None:
    assert ent is not None
    ui_elem = esper.component_for_entity(ent, UIElementComponent)
    ui_elem.button_val = not ui_elem.button_val


def toggle_sound(ent: ActionArgs) -> None:
    flip_ui_elem_val(ent)
    assert ent is not None
    ui_elem = esper.component_for_entity(ent, UIElementComponent)
    assert isinstance(ui_elem.button_val, bool)
    SETTINGS_REF.GAME_MUTE = ui_elem.button_val


def set_slider_val(ent: ActionArgs) -> None:
    assert ent is not None
    ui_elem = esper.component_for_entity(ent, UIElementComponent)
    bb = esper.component_for_entity(ent, BoundingBox)

    mx, my = get_mouse_pos_in_px()

    t_size = SETTINGS_REF.BUTTON_TILE_SIZE
    if bb.width < t_size + 1:
        w = bb.height - t_size
        t = (my - bb.top - t_size / 2) / w
    else:
        w = bb.width - t_size
        t = (mx - bb.left - t_size / 2) / w

    ui_elem.button_val = min(1.0, max(0.0, t))
