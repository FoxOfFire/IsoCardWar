from dataclasses import dataclass


@dataclass
class PlayerData:
    start_of_turn_draw_count: int = 5


PLAYER_DATA_REF = PlayerData
