from dataclasses import dataclass
from typing import Callable, Optional

import pygame

from .enums import UIStateEnum
from .log import logger


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


def _empty_text() -> str:
    return " "


class MaskedSprite:
    mask: pygame.Mask = pygame.Mask((1, 1), fill=True)
    rect: pygame.Rect = pygame.Rect(0, 0, 1, 1)


@dataclass
class CardSprite(MaskedSprite):
    pass


def noop(ent: int) -> None:
    logger.info(f"entity: {ent} clicked")


@dataclass
class UIElementComponent:
    state: UIStateEnum = UIStateEnum.BASE
    is_visible: bool = True
    is_clickable: bool = True
    is_active: bool = False
    is_part_of_game_ui: bool = False
    text: Callable[[], str] = _empty_text
    click_func: Optional[Callable[..., None]] = None
