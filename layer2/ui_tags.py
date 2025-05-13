from dataclasses import dataclass
from typing import Callable, Optional

from .enums import UIStateEnum


class Plain:
    """
    Designates plain type bounding boxes
    """


class GameCameraTag:
    pass


class IsoCameraTag:
    pass


def _empty_text() -> str:
    return " "


@dataclass
class UIElementComponent:
    state: UIStateEnum = UIStateEnum.BASE
    is_visible: bool = True
    is_clickable: bool = True
    is_active: bool = False
    is_part_of_game_ui: bool = False
    text: Callable[[], str] = _empty_text
    click_func: Optional[Callable[..., None]] = None
