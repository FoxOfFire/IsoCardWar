import esper

from .state import STATE_REF
from .state_utils import ActionArgs


def end_player_phase_action(_: ActionArgs = None) -> None:
    STATE_REF.end_player_phase = True


def remove_hover(_: ActionArgs = None) -> None:
    STATE_REF.selecting = None


def unselect(_: ActionArgs = None) -> None:
    STATE_REF.selected = None


def play_card(ent: ActionArgs) -> None:
    assert STATE_REF.play_card_func is not None
    STATE_REF.play_card_func(ent)


def select(ent: ActionArgs) -> None:
    assert ent is not None
    assert esper.entity_exists(ent)
    STATE_REF.selected = ent


def hover(ent: ActionArgs) -> None:
    assert ent is not None
    assert esper.entity_exists(ent)
    STATE_REF.selecting = ent
