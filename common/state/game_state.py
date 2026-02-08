from typing import Dict, Optional

from .game_state_utils import (
    Action,
    GamePhaseEnum,
    PriceEnum,
)


class GameState:
    def __init__(self) -> None:
        self.resources: Dict[PriceEnum, int] = {}
        self.play_card_func: Optional[Action] = None
        self.selected: Optional[int] = None
        self.selecting: Optional[int] = None
        self.game_phase: GamePhaseEnum = GamePhaseEnum.BEGIN_GAME
        self.end_player_phase: bool = False


GAME_STATE_REF = GameState()
