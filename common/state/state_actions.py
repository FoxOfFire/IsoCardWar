import esper

from .state import STATE_REF
from .state_utils import Action, ActionArgs


def end_player_phase_action(_: ActionArgs = None) -> None:
    STATE_REF.end_player_phase = True


def play_card(ent: ActionArgs) -> None:
    assert STATE_REF.play_card_func is not None
    STATE_REF.play_card_func(ent)


def select(ent: ActionArgs) -> None:
    assert ent is None or esper.entity_exists(ent)
    STATE_REF.selected = ent


def hover(ent: ActionArgs) -> None:
    assert ent is None or esper.entity_exists(ent)
    STATE_REF.selecting = ent


def target(ent: ActionArgs) -> None:
    assert ent is None or esper.entity_exists(ent)
    STATE_REF.target_tile = ent


def get_set_target_action(ent: ActionArgs) -> Action:
    return lambda _: target(ent)
