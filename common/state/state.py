from dataclasses import dataclass
from typing import Dict, Optional

from .state_utils import (
    Action,
    GamePhaseType,
    PriceEnum,
)


@dataclass
class GameState:
    resources: Dict[PriceEnum, int]
    play_card_func: Optional[Action] = None
    selected_card: Optional[int] = None
    selected_tile: Optional[int] = None
    hovered_ent: Optional[int] = None
    game_phase: GamePhaseType = GamePhaseType.BEGIN_GAME
    end_player_phase: bool = False


DEFAULT_RESOURCES: Dict[PriceEnum, int] = {
    PriceEnum.MANA: 3,
    PriceEnum.HERBS: 2,
    PriceEnum.BLOOD: 0,
}

STATE_REF = GameState(DEFAULT_RESOURCES)
