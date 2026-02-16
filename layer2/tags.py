from dataclasses import dataclass
from typing import List, Optional, Tuple

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


class TextCameraTag:
    pass


class MaskedSprite:
    mask: pygame.Mask = pygame.Mask((1, 1), fill=True)
    rect: pygame.Rect = pygame.Rect(0, 0, 1, 1)


@dataclass
class TextData:
    text: TextFunc
    offset: Tuple[float, float]


@dataclass
class UIElementComponent:
    click_func: List[Action]
    start_hover_func: List[Action]
    end_hover_func: List[Action]
    hover_func: List[Action]
    text: List[TextData]
    state: UIStateEnum = UIStateEnum.BASE
    button_val: Optional[bool | float] = None
    is_visible: bool = True
    is_clickable: bool = True
    is_active: bool = False
    is_gameplay_elem: bool = False
