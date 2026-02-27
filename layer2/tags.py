from dataclasses import dataclass
from typing import Any, List, Optional, Tuple

import pygame

from common import Action, TextFunc

from .enums import UIStateEnum


class GameCameraTag:
    pass


class MaskedSprite:
    mask: pygame.Mask
    rect: pygame.Rect

    def __init__(self, rect: Optional[pygame.Rect] = None) -> None:
        if rect is None:
            self.rect = pygame.Rect((0, 0), (1, 1))
            self.mask = pygame.Mask((1, 1), fill=True)
        else:
            self.rect = rect
            self.mask = pygame.Mask(rect.size, fill=False)
            self.mask.fill()


@dataclass
class TextData:
    text: TextFunc
    offset: Tuple[float, float]


@dataclass
class UIElementComponent:
    click_start_func: List[Action]
    click_func: List[Action]
    clicking_func: List[Action]
    click_cancel_func: List[Action]
    start_hover_func: List[Action]
    hover_func: List[Action]
    end_hover_func: List[Action]
    text: List[TextData]
    state: UIStateEnum = UIStateEnum.BASE
    button_val: Optional[bool | float] = None
    parent_elem: Optional[Any] = None
    is_visible: bool = True
    is_clickable: bool = True
    is_active: bool = False
    is_gameplay_elem: bool = False
