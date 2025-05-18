from typing import Tuple

import esper
import pygame

from common import BoundingBox
from layer1.iso_map import map_obj
from layer2.tags import GameCameraTag

from .log import logger

SWITCH_SCENE = pygame.event.custom_type()


class SelectionException(Exception):
    pass


# /\       T~~T
# /  \ ---\ |  |
# \  / ---/ |  |
# \/       L__J
def _get_transformed_mouse_pos(bb: BoundingBox) -> Tuple[float, float]:
    cam_bb = esper.component_for_entity(
        esper.get_component(GameCameraTag)[0][0], BoundingBox
    )

    display_rect = pygame.display.get_surface().get_rect()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    map_width, map_height = map_obj.size

    x = (mouse_x * cam_bb.width / display_rect.width - bb.left) / bb.width
    y = (mouse_y * cam_bb.height / display_rect.height - bb.top) / bb.height

    calc_x = (x - y + 1 / 2) * map_width
    calc_y = (y + x - 1 / 2) * map_height

    return calc_x, calc_y


def click_on_tile(ent: int, mouse: Tuple[float, float]) -> None:
    bb = esper.component_for_entity(ent, BoundingBox)

    logger.info(_get_transformed_mouse_pos(bb))
