
from dataclasses import dataclass
from typing import Callable, Optional

import esper

from .enums import UIStateEnum

worlds_with_camera = set[str]()


class UniqueUIElementCreatedTwiceException(Exception):
    pass


class Camera:
    """
    # Camera tag

    the tag that denotes if an element is the camera

    there sould only ever be one entity with this tag
    """

    def __init__(self) -> None:
        global worlds_with_camera
        if esper.current_world in worlds_with_camera:
            raise UniqueUIElementCreatedTwiceException()
        else:
            worlds_with_camera.add(esper.current_world)


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
    click_funcs: Optional[Callable[..., None]] = None
