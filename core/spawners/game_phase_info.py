from functools import partial
from typing import Dict, List

from common import Action
from layer1 import GamePhaseEnum, draw_cards


def _begin_game() -> List[Action]:
    effects: List[Action] = []
    return effects


def _draw() -> List[Action]:
    effects: List[Action] = []
    for func in draw_cards(1):
        effects.append(partial(func, None, None))
    return effects


def _end_of_turn() -> List[Action]:
    effects: List[Action] = []
    return effects


def _enemy_action() -> List[Action]:
    effects: List[Action] = []
    return effects


def _end_game() -> List[Action]:
    effects: List[Action] = []
    return effects


def _player_action() -> List[Action]:
    effects: List[Action] = []
    # TODO
    return effects


def get_base_game_phase_dict() -> Dict[GamePhaseEnum, List[Action]]:
    return {
        GamePhaseEnum.BEGIN_GAME: _begin_game(),
        GamePhaseEnum.DRAW: _draw(),
        GamePhaseEnum.PLAYER_ACTION: _player_action(),
        GamePhaseEnum.END_OF_TURN: _end_of_turn(),
        GamePhaseEnum.ENEMY_ACTION: _enemy_action(),
        GamePhaseEnum.END_GAME: _end_game(),
    }
