from dataclasses import dataclass
from typing import Dict, Optional

from .state_utils import Action, GamePhaseType, PriceEnum


@dataclass
class GameState:
    resources: Dict[PriceEnum, int]
    play_card_func: Optional[Action] = None
    selected_card: Optional[int] = None
    selected_tile: Optional[int] = None
    hovered_ent: Optional[int] = None
    game_phase: GamePhaseType = GamePhaseType.INIT
    end_player_phase: bool = False


DEFAULT_RESOURCES: Dict[PriceEnum, int] = {
    PriceEnum.MANA: 99,
    PriceEnum.HERBS: 99,
    PriceEnum.BLOOD: 99,
    PriceEnum.BREW: 99,
}

STATE_REF = GameState(DEFAULT_RESOURCES)
