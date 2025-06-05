from collections.abc import Callable
from typing import Dict, Optional

import esper

from .game_state_utils import GamePhaseEnum, PriceEnum


class GameState:
    def __init__(self) -> None:
<<<<<<< HEAD
        self.resources: Dict[PriceEnum, int] = {}
        self.play_card: Optional[Callable[[int], None]] = None
        self.get_selected: Optional[Callable[[], int]] = None
        self.selected: Optional[int] = None
        self.selecting: Optional[int] = None
        self.game_phase: GamePhaseEnum = GamePhaseEnum.BEGIN_GAME
        self.end_player_phase: bool = False
=======
        self.resources: Dict[PriceEnum, int]
        self.play_card: Optional[Callable[[int], None]]
        self.get_selected: Optional[Callable[[], int]]
        self.selected: Optional[int] = None
        self.selecting: Optional[int] = None
        self.game_phase: GamePhaseEnum = GamePhaseEnum.BEGIN_GAME
>>>>>>> master


GAME_STATE_REF = GameState()


# cards
def set_play_card(func: Callable[[int], None]) -> None:
    GAME_STATE_REF.play_card = func


def play_card(target: int) -> None:
    if GAME_STATE_REF.play_card is None:
        return
    GAME_STATE_REF.play_card(target)


def remove_hover(_: int) -> None:
<<<<<<< HEAD
    GAME_STATE_REF.selecting = None


def unselect() -> None:
    GAME_STATE_REF.selected = None
=======
    game_state_obj.selecting = None


def unselect() -> None:
    game_state_obj.selected = None
>>>>>>> master


def select(ent: int) -> None:
    if not esper.entity_exists(ent):
        return
<<<<<<< HEAD
    GAME_STATE_REF.selected = ent
=======
    game_state_obj.selected = ent
>>>>>>> master


def hover(ent: int) -> None:
    if not esper.entity_exists(ent):
        return
<<<<<<< HEAD
    GAME_STATE_REF.selecting = ent
=======
    game_state_obj.selecting = ent
>>>>>>> master
