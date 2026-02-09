import esper

from .game_state import GAME_STATE_REF
from .game_state_utils import ActionArgs


def end_player_phase_action(_: ActionArgs = None) -> None:
    GAME_STATE_REF.end_player_phase = True


def remove_hover(_: ActionArgs = None) -> None:
    GAME_STATE_REF.selecting = None


def unselect(_: ActionArgs = None) -> None:
    GAME_STATE_REF.selected = None


def play_card(args: ActionArgs) -> None:
    assert args is not None
    target, card_num = args
    assert GAME_STATE_REF.play_card_func is not None
    GAME_STATE_REF.play_card_func((target, card_num))


def select(args: ActionArgs) -> None:
    assert args is not None
    ent, _ = args
    assert ent is not None
    assert esper.entity_exists(ent)
    GAME_STATE_REF.selected = ent


def hover(args: ActionArgs) -> None:
    assert args is not None
    ent, _ = args
    assert ent is not None
    assert esper.entity_exists(ent)
    GAME_STATE_REF.selecting = ent
