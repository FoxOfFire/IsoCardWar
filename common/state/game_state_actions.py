from typing import Optional

import esper

from .game_state import GAME_STATE_REF
from .game_state_utils import ActionDecor


@ActionDecor
def end_player_phase_action(_: Optional[int], __: Optional[int]) -> None:
    GAME_STATE_REF.end_player_phase = True


@ActionDecor
def remove_hover(_: Optional[int], __: Optional[int]) -> None:
    GAME_STATE_REF.selecting = None


@ActionDecor
def unselect(_: Optional[int], __: Optional[int]) -> None:
    GAME_STATE_REF.selected = None


@ActionDecor
def play_card(target: Optional[int], card_num: Optional[int]) -> None:
    if GAME_STATE_REF.play_card_func is None:
        return
    GAME_STATE_REF.play_card_func(target, card_num)


@ActionDecor
def select(ent: Optional[int], _: Optional[int]) -> None:
    assert ent is not None
    assert esper.entity_exists(ent)
    GAME_STATE_REF.selected = ent


@ActionDecor
def hover(ent: Optional[int], _: Optional[int]) -> None:
    assert ent is not None
    assert esper.entity_exists(ent)
    GAME_STATE_REF.selecting = ent
