from functools import partial
from typing import Callable, Dict, List, Optional

import esper

from common import (
    SETTINGS_REF,
    Action,
    GamePhaseType,
    get_select_tile_action,
    reset_trigger,
    turn_counter_plus_one_action,
)
from layer1 import (
    MAP_DATA_REF,
    Tile,
    UnitTypeEnum,
    discard_hand,
    draw_card,
    get_wait_ms_action,
    reset_active_tile,
    set_active_tile,
)

from .log import logger


def _begin_game() -> List[Action]:
    effects: List[Action] = [
        reset_trigger,
        get_wait_ms_action(500),
    ]
    return effects


def _production() -> List[Action]:
    effects: List[Action] = [
        reset_trigger,
        turn_counter_plus_one_action,
        get_wait_ms_action(75),
    ]
    return _enemy_action(MAP_DATA_REF.get_productions_for_type) + effects


def _draw() -> List[Action]:
    effects: List[Action] = [
        reset_trigger,
        draw_card,
        get_wait_ms_action(75),
        draw_card,
        get_wait_ms_action(75),
        draw_card,
        get_wait_ms_action(75),
        draw_card,
        get_wait_ms_action(75),
        draw_card,
        reset_active_tile,
    ]
    return effects


def _player_action() -> List[Action]:
    effects: List[Action] = [
        reset_trigger,
    ]
    # TODO
    return effects


def _end_of_turn() -> List[Action]:
    effects: List[Action] = [
        reset_trigger,
        discard_hand,
    ]
    return effects


def _enemy_action(
    actions: Callable[[Optional[UnitTypeEnum]], List[Action]],
) -> List[Action]:
    effects: List[Action] = [reset_trigger]
    for w in range(SETTINGS_REF.ISO_MAP_WIDTH):
        for h in range(SETTINGS_REF.ISO_MAP_HEIGHT):
            tile = MAP_DATA_REF.ent_at((h, w))
            unit = esper.component_for_entity(tile, Tile).unit
            tile_effects = actions(unit)

            if len(tile_effects) < 1:
                continue

            effects += tile_effects

            effects.append(set_active_tile)
            effects.append(get_select_tile_action(tile))
            effects.append(reset_trigger)
    return effects


def _end_game() -> List[Action]:
    effects: List[Action] = [
        reset_trigger,
    ]
    return effects


def _spawning() -> List[Action]:
    effects: List[Action] = [
        reset_trigger,
        get_wait_ms_action(500),
    ]
    return effects


def get_base_game_phase_dict() -> (
    Dict[GamePhaseType, Callable[[], List[Action]]]
):
    logger.info("getting phase dict")
    return {
        GamePhaseType.BEGIN_GAME: _begin_game,
        GamePhaseType.TELEGRAPH: partial(
            _enemy_action, MAP_DATA_REF.get_actions_for_type
        ),
        GamePhaseType.PRODUCTION: _production,
        GamePhaseType.SPAWNING: _spawning,
        GamePhaseType.TELEGRAPH: partial(
            _enemy_action, MAP_DATA_REF.get_telegraphs_for_type
        ),
        GamePhaseType.DRAW: _draw,
        GamePhaseType.PLAYER_ACTION: _player_action,
        GamePhaseType.END_OF_TURN: _end_of_turn,
        GamePhaseType.ENEMY_ACTION: partial(
            _enemy_action, MAP_DATA_REF.get_actions_for_type
        ),
        GamePhaseType.END_GAME: _end_game,
    }
