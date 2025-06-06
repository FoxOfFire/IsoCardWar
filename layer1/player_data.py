from dataclasses import dataclass


@dataclass
class PlayerData:
    start_of_game_draw_count: int = 5


PLAYER_DATA_REF = PlayerData
