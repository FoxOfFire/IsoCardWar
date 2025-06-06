from collections.abc import Callable
from typing import Dict, Optional

import esper

from common.types import EntityFunc

from .game_state_utils import GamePhaseEnum, PriceEnum


class GameState:
    def __init__(self) -> None:
        self.resources: Dict[PriceEnum, int] = {}
        self.play_card: Optional[EntityFunc] = None
        self.get_selected: Optional[Callable[[], int]] = None
        self.selected: Optional[int] = None
        self.selecting: Optional[int] = None
        self.game_phase: GamePhaseEnum = GamePhaseEnum.BEGIN_GAME
        self.end_player_phase: bool = False


GAME_STATE_REF = GameState()


# cards
def set_play_card(func: EntityFunc) -> None:
    GAME_STATE_REF.play_card = func


def play_card(target: int) -> None:
    if GAME_STATE_REF.play_card is None:
        return
    GAME_STATE_REF.play_card(target)


def remove_hover(_: int) -> None:
    GAME_STATE_REF.selecting = None


def unselect() -> None:
    GAME_STATE_REF.selected = None


def select(ent: int) -> None:
    if not esper.entity_exists(ent):
        return
    GAME_STATE_REF.selected = ent


def hover(ent: int) -> None:
    if not esper.entity_exists(ent):
        return
    GAME_STATE_REF.selecting = ent
