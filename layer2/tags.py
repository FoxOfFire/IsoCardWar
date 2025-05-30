from collections.abc import Callable
from dataclasses import dataclass
from typing import List, NamedTuple, Optional, Tuple

import pygame

from .enums import UIStateEnum


class TrackUI(NamedTuple):
    pass


class TrackIso(NamedTuple):
    pass


class Plain:
    """
    Designates plain type bounding boxes
    """


class GameCameraTag:
    pass


class IsoCameraTag:
    pass


class TextCameraTag:
    pass


class MaskedSprite:
    mask: pygame.Mask = pygame.Mask((1, 1), fill=True)
    rect: pygame.Rect = pygame.Rect(0, 0, 1, 1)


@dataclass
class TextData:
    text: Callable[[], str]
    offset: Tuple[float, float]


class UIElementComponent:
    def __init__(
        self,
        state: UIStateEnum = UIStateEnum.BASE,
        is_visible: bool = True,
        is_clickable: bool = True,
        is_active: bool = False,
        text: Optional[List[TextData]] = None,
        click_func: Optional[Callable[[int], None]] = None,
        hover_func: Optional[Callable[[int], None]] = None,
        unhover_func: Optional[Callable[[int], None]] = None,
    ):
        self.state: UIStateEnum = state
        self.is_visible: bool = is_visible
        self.is_clickable: bool = is_clickable
        self.is_active: bool = is_active
        self.text: List[TextData] = [] if text is None else text
        self.click_func: Optional[Callable[[int], None]] = click_func
        self.hover_func: Optional[Callable[[int], None]] = hover_func
        self.unhover_func: Optional[Callable[[int], None]] = unhover_func
