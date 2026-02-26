from dataclasses import dataclass
from typing import Any, List, Optional, Tuple

import pygame

from common import Action, TextFunc, TrackBase

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


class MaskedSprite:
    mask: pygame.Mask
    rect: pygame.Rect

    def __init__(
        self,
        top_left: Tuple[float, float] = (0, 0),
        size: Tuple[float, float] = (1, 1),
    ) -> None:
        print(top_left, size)
        self.mask = pygame.Mask(size, fill=True)
        self.rect = pygame.Rect(top_left, size)


@dataclass
class TextData:
    text: TextFunc
    offset: Tuple[float, float]


@dataclass
class UIElementComponent:
    click_func: List[Action]
    clicking_func: List[Action]
    click_cancel_func: List[Action]
    start_hover_func: List[Action]
    end_hover_func: List[Action]
    hover_func: List[Action]
    text: List[TextData]
    state: UIStateEnum = UIStateEnum.BASE
    button_val: Optional[bool | float] = None
    parent_elem: Optional[Any] = None
    is_visible: bool = True
    is_clickable: bool = True
    is_active: bool = False
    is_gameplay_elem: bool = False
