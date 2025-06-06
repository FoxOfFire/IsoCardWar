from layer1.game_phase import end_player_phase
from layer2.rendering import UIElemType
from layer2.ui import quit_game

from .spawner_ui import spawn_button
from .text_functions import get_fps_str, get_game_phase_str


def build_ui() -> None:
    spawn_button((5, 5), get_fps_str, UIElemType.TEXTBOX)
    spawn_button((74, 5), get_game_phase_str, UIElemType.TEXTBOX)
    spawn_button((5, 65), "Quit", UIElemType.BUTTON, click_func=quit_game)
    spawn_button(
        (5, 50),
        "End Turn",
        UIElemType.BUTTON,
        click_func=end_player_phase,
    )
