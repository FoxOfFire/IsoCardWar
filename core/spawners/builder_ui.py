from layer2.rendering import UIElemType
from layer2.ui import quit_game

from .spawner_ui import spawn_button
from .text_functions import get_fps_str


def build_ui() -> None:
    spawn_button((5, 5), get_fps_str, UIElemType.TEXTBOX)
    spawn_button((5, 20), "Quit", UIElemType.BUTTON, click_func=quit_game)
