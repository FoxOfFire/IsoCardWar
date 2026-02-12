import esper

from .state import STATE_REF
from .state_utils import Action, ActionArgs


def end_player_phase_action(_: ActionArgs = None) -> None:
    STATE_REF.end_player_phase = True


def play_card(ent: ActionArgs) -> None:
    assert STATE_REF.play_card_func is not None
    STATE_REF.play_card_func(ent)


def select_card(ent: ActionArgs) -> None:
    assert ent is None or esper.entity_exists(ent)
    STATE_REF.selected_card = ent


def hover(ent: ActionArgs) -> None:
    assert ent is None or esper.entity_exists(ent)
    STATE_REF.hovered_ent = ent


def select_tile(ent: ActionArgs) -> None:
    assert ent is None or esper.entity_exists(ent)
    STATE_REF.selected_tile = ent


def get_select_tile_action(ent: ActionArgs) -> Action:
    return lambda _: select_tile(ent)
