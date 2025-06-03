from collections.abc import Callable
from functools import partial
from typing import Dict, List

from layer1 import GamePhaseEnum
from layer1.cards import draw_cards


def _begin_game() -> List[Callable[[], None]]:
    effects: List[Callable[[], None]] = []
    return effects


def _draw() -> List[Callable[[], None]]:
    effects: List[Callable[[], None]] = []
    for func in draw_cards(1):
        effects.append(partial(func, -1, -1))
    return effects


def _end_of_turn() -> List[Callable[[], None]]:
    effects: List[Callable[[], None]] = []
    return effects


def _enemy_action() -> List[Callable[[], None]]:
    effects: List[Callable[[], None]] = []
    return effects


def _end_game() -> List[Callable[[], None]]:
    effects: List[Callable[[], None]] = []
    return effects


def get_base_game_phase_dict() -> Dict[GamePhaseEnum, List[Callable[[], None]]]:
    return {
        GamePhaseEnum.BEGIN_GAME: _begin_game(),
        GamePhaseEnum.DRAW: _draw(),
        GamePhaseEnum.PLAYER_ACTION: [],
        GamePhaseEnum.END_OF_TURN: _end_of_turn(),
        GamePhaseEnum.ENEMY_ACTION: _enemy_action(),
        GamePhaseEnum.END_GAME: _end_game(),
    }
