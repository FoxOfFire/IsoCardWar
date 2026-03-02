import esper
import pygame

from common import (
    SETTINGS_REF,
    STATE_REF,
    Action,
    ActionDecor,
    ActionEnt,
    BoundingBox,
    discard_trigger_effect,
)
from layer2.tags import UIElementComponent

from .audio import SoundTypeEnum, play_sfx
from .ui_utils import get_mouse_pos_in_px


def get_sound_action(sound: SoundTypeEnum) -> Action:
    return discard_trigger_effect(ActionDecor(lambda _: play_sfx(sound)))


def card_guard(action: Action) -> Action:
    @ActionDecor
    def sub_acton(ent: ActionEnt) -> bool:
        if STATE_REF.selected_card is None or ent is None:
            return False
        return action(ent, True)

    return sub_acton


@ActionDecor
def quit_game(_: ActionEnt = None) -> bool:
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    return True


@ActionDecor
def flip_ui_elem_val(ent: ActionEnt) -> bool:
    if ent is None:
        return False
    ui_elem = esper.component_for_entity(ent, UIElementComponent)
    ui_elem.button_val = not ui_elem.button_val
    return True


@ActionDecor
def toggle_sound(ent: ActionEnt) -> bool:
    if ent is None or not flip_ui_elem_val(ent, True):
        return False
    ui_elem = esper.component_for_entity(ent, UIElementComponent)
    if not isinstance(ui_elem.button_val, bool):
        return False
    SETTINGS_REF.GAME_MUTE = ui_elem.button_val
    return True


@ActionDecor
def set_slider_val(ent: ActionEnt) -> bool:
    if ent is None:
        return False
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
    return True
