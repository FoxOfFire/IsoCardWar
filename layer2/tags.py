from dataclasses import dataclass
from typing import List, Tuple

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


class UIElementComponent:
    def __init__(
        self,
        *,
        click_func: List[Action],
        hover_func: List[Action],
        unhover_func: List[Action],
        text: List[TextData],
        state: UIStateEnum = UIStateEnum.BASE,
        is_visible: bool = True,
        is_clickable: bool = True,
        is_active: bool = False,
        is_gameplay_elem: bool = False,
    ):
        self.text: List[TextData] = text
        self.click_func: List[Action] = click_func
        self.hover_func: List[Action] = unhover_func
        self.unhover_func: List[Action] = hover_func

        self.state: UIStateEnum = state
        self.is_visible: bool = is_visible
        self.is_clickable: bool = is_clickable
        self.is_active: bool = is_active
        self.is_gameplay_elem = is_gameplay_elem
