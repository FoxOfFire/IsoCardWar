from dataclasses import dataclass
from typing import Dict, Optional

from .state_utils import (
    Action,
    GamePhaseEnum,
    PriceEnum,
)


@dataclass
class GameState:
    resources: Dict[PriceEnum, int]
    play_card_func: Optional[Action] = None
    selected: Optional[int] = None
    selecting: Optional[int] = None
    game_phase: GamePhaseEnum = GamePhaseEnum.BEGIN_GAME
    end_player_phase: bool = False


STATE_REF = GameState({})
