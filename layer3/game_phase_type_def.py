from functools import partial
from typing import Callable, Dict, List

import esper

from common import (
    SETTINGS_REF,
    Action,
    GamePhaseType,
    get_select_tile_action,
    reset_trigger,
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
    effects: List[Action] = [
        get_wait_ms_action(2000),
    ]
    return effects


def _production() -> List[Action]:
    effects: List[Action] = []
    return effects


def _draw() -> List[Action]:
    effects: List[Action] = [
        draw_card,
        get_wait_ms_action(75),
        draw_card,
        get_wait_ms_action(75),
        draw_card,
        get_wait_ms_action(75),
        draw_card,
        get_wait_ms_action(75),
        draw_card,
    ]
    return effects


def _player_action() -> List[Action]:
    effects: List[Action] = []
    # TODO
    return effects


def _end_of_turn() -> List[Action]:
    effects: List[Action] = [
        discard_hand,
    ]
    return effects


def _enemy_action(telegraphs: bool) -> List[Action]:
    effects: List[Action] = []
    for w in range(SETTINGS_REF.ISO_MAP_WIDTH):
        for h in range(SETTINGS_REF.ISO_MAP_HEIGHT):
            tile = MAP_DATA_REF.ent_at((h, w))
            unit = esper.component_for_entity(tile, Tile).unit
            if telegraphs:
                tile_effects = MAP_DATA_REF.get_telegraphs_for_type(unit)
            else:
                tile_effects = MAP_DATA_REF.get_actions_for_type(unit)

            if len(tile_effects) < 1:
                continue

            effects += tile_effects

            effects.append(get_select_tile_action(tile))
            effects.append(reset_trigger)
    return effects


def _end_game() -> List[Action]:
    effects: List[Action] = []
    return effects


def get_base_game_phase_dict() -> (
    Dict[GamePhaseType, Callable[[], List[Action]]]
):
    logger.info("getting phase dict")
    return {
        GamePhaseType.BEGIN_GAME: _begin_game,
        GamePhaseType.TELEGRAPH: partial(_enemy_action, True),
        GamePhaseType.PRODUCTION: _production,
        GamePhaseType.DRAW: _draw,
        GamePhaseType.PLAYER_ACTION: _player_action,
        GamePhaseType.END_OF_TURN: _end_of_turn,
        GamePhaseType.ENEMY_ACTION: partial(_enemy_action, False),
        GamePhaseType.END_GAME: _end_game,
    }
