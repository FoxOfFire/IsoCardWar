from dataclasses import dataclass
from typing import List, Optional, Tuple

import pygame

from common.position_tracking.tags import TrackBase
from common.types import ButtonFunc, TextFunc

from .enums import UIStateEnum


class TrackUI(TrackBase):
    def __str__(self) -> str:
        return "TrackUI"


class TrackIso(TrackBase):
    def __str__(self) -> str:
        return "TrackISO"


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
    text: TextFunc
    offset: Tuple[float, float]


class UIElementComponent:
    def __init__(
        self,
        state: UIStateEnum = UIStateEnum.BASE,
        is_visible: bool = True,
        is_clickable: bool = True,
        is_active: bool = False,
        is_gameplay_elem: bool = False,
        text: Optional[List[TextData]] = None,
        click_func: Optional[ButtonFunc] = None,
        hover_func: Optional[ButtonFunc] = None,
        unhover_func: Optional[ButtonFunc] = None,
    ):
        self.state: UIStateEnum = state
        self.is_visible: bool = is_visible
        self.is_clickable: bool = is_clickable
        self.is_active: bool = is_active
        self.is_gameplay_elem = is_gameplay_elem
        self.text: List[TextData] = [] if text is None else text
        self.click_func: Optional[ButtonFunc] = click_func
        self.hover_func: Optional[ButtonFunc] = hover_func
        self.unhover_func: Optional[ButtonFunc] = unhover_func
