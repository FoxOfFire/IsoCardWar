from typing import Callable, Dict, List

import esper

from common import (
    SETTINGS_REF,
    Action,
    GamePhaseEnum,
    get_select_tile_action,
)
from layer1 import (
    MAP_DATA_REF,
    Tile,
    discard_hand,
    draw_card,
    get_wait_ms_action,
)

from .log import logger


def _begin_game() -> List[Action]:
    effects: List[Action] = []
    return effects


def _draw() -> List[Action]:
    effects: List[Action] = [
        draw_card,
        get_wait_ms_action(50),
        draw_card,
        get_wait_ms_action(50),
        draw_card,
        get_wait_ms_action(50),
        draw_card,
        get_wait_ms_action(50),
        draw_card,
        get_wait_ms_action(50),
    ]
    return effects


def _end_of_turn() -> List[Action]:
    effects: List[Action] = [
        discard_hand,
    ]
    return effects


def _enemy_action() -> List[Action]:
    effects: List[Action] = []
    for w in range(SETTINGS_REF.ISO_MAP_WIDTH):
        for h in range(SETTINGS_REF.ISO_MAP_HEIGHT):
            tile = MAP_DATA_REF.ent_at((h, w))
            unit = esper.component_for_entity(tile, Tile).unit
            tile_effects = MAP_DATA_REF.get_actions_for_type(unit)

            if len(tile_effects) < 1:
                continue

            effects.append(get_select_tile_action(tile))
            for effect in tile_effects:
                effects.append(effect)
            effects.append(get_wait_ms_action(50))
            effects.append(get_select_tile_action(tile))
    return effects


def _end_game() -> List[Action]:
    effects: List[Action] = []
    return effects


def _player_action() -> List[Action]:
    effects: List[Action] = []
    # TODO
    return effects


def get_base_game_phase_dict() -> (
    Dict[GamePhaseEnum, Callable[[], List[Action]]]
):
    return {
        GamePhaseEnum.BEGIN_GAME: _begin_game,
        GamePhaseEnum.DRAW: _draw,
        GamePhaseEnum.PLAYER_ACTION: _player_action,
        GamePhaseEnum.END_OF_TURN: _end_of_turn,
        GamePhaseEnum.ENEMY_ACTION: _enemy_action,
        GamePhaseEnum.END_GAME: _end_game,
    }
