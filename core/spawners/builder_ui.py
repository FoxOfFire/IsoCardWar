from layer2.rendering import UIElemType

from .spawner_ui import spawn_button
from .text_functions import get_fps_str


def build_ui() -> None:
    spawn_button((5, 5), get_fps_str, UIElemType.TEXTBOX)
    spawn_button((5, 20), "Cocking", UIElemType.BUTTON)
