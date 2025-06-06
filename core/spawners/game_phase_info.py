from functools import partial
from typing import Dict, List

from common.types import PhaseFunc
from layer1 import GamePhaseEnum
from layer1.cards import draw_cards


def _begin_game() -> List[PhaseFunc]:
    effects: List[PhaseFunc] = []
    return effects


def _draw() -> List[PhaseFunc]:
    effects: List[PhaseFunc] = []
    for func in draw_cards(1):
        effects.append(partial(func, -1, -1))
    return effects


def _end_of_turn() -> List[PhaseFunc]:
    effects: List[PhaseFunc] = []
    return effects


def _enemy_action() -> List[PhaseFunc]:
    effects: List[PhaseFunc] = []
    return effects


def _end_game() -> List[PhaseFunc]:
    effects: List[PhaseFunc] = []
    return effects


def _player_action() -> List[PhaseFunc]:
    effects: List[PhaseFunc] = []

    err = "player actions should be decided by the player why was this called?"

    def error() -> None:
        raise RuntimeError(err)

    effects.append(error)
    return effects


def get_base_game_phase_dict() -> Dict[GamePhaseEnum, List[PhaseFunc]]:
    return {
        GamePhaseEnum.BEGIN_GAME: _begin_game(),
        GamePhaseEnum.DRAW: _draw(),
        GamePhaseEnum.PLAYER_ACTION: _player_action(),
        GamePhaseEnum.END_OF_TURN: _end_of_turn(),
        GamePhaseEnum.ENEMY_ACTION: _enemy_action(),
        GamePhaseEnum.END_GAME: _end_game(),
    }
