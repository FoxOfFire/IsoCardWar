from typing import Dict, List, Optional

import esper

from common import Action, EntityFunc

from .game_state_utils import GamePhaseEnum, PriceEnum


class GameState:
    def __init__(self) -> None:
        self.resources: Dict[PriceEnum, int] = {}
        self.play_card_func: Optional[EntityFunc] = None
        self.selected: Optional[int] = None
        self.selecting: Optional[int] = None
        self.game_phase: GamePhaseEnum = GamePhaseEnum.BEGIN_GAME
        self.end_player_phase: bool = False
        self.action_queue: Dict[GamePhaseEnum, List[Action]] = {}

    def play_card(
        self, target: Optional[int], card_num: Optional[int]
    ) -> None:
        if GAME_STATE_REF.play_card_func is None:
            return
        GAME_STATE_REF.play_card_func(target, card_num)

    def end_player_phase_action(self) -> None:
        GAME_STATE_REF.end_player_phase = True

    def remove_hover(self) -> None:
        GAME_STATE_REF.selecting = None

    def unselect(self) -> None:
        GAME_STATE_REF.selected = None

    def select(self, ent: Optional[int], _: Optional[int]) -> None:
        assert ent is not None
        assert esper.entity_exists(ent)
        GAME_STATE_REF.selected = ent

    def hover(self, ent: Optional[int], _: Optional[int]) -> None:
        assert ent is not None
        assert esper.entity_exists(ent)
        GAME_STATE_REF.selecting = ent


GAME_STATE_REF = GameState()
