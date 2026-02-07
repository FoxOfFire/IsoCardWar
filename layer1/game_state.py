from typing import Dict, List, Optional

import esper

from common import Action, EntityFunc

from .game_state_utils import GamePhaseEnum, PriceEnum


class GameState:
    def __init__(self) -> None:
        self.resources: Dict[PriceEnum, int] = {}
        self.play_card: Optional[EntityFunc] = None
        self.selected: Optional[int] = None
        self.selecting: Optional[int] = None
        self.game_phase: GamePhaseEnum = GamePhaseEnum.BEGIN_GAME
        self.end_player_phase: bool = False
        self.phase_funk_queue: Dict[GamePhaseEnum, List[Action]] = {}


GAME_STATE_REF = GameState()


# cards
def set_play_card(func: EntityFunc) -> None:
    GAME_STATE_REF.play_card = func


def play_card(target: int, card_num: int) -> None:
    if GAME_STATE_REF.play_card is None:
        return
    GAME_STATE_REF.play_card(target, card_num)


def remove_hover(_: int, __: int) -> None:
    GAME_STATE_REF.selecting = None


def unselect() -> None:
    GAME_STATE_REF.selected = None


def select(ent: int, _: int) -> None:
    assert esper.entity_exists(ent)
    GAME_STATE_REF.selected = ent


def hover(ent: int, _: int) -> None:
    assert esper.entity_exists(ent)
    GAME_STATE_REF.selecting = ent
