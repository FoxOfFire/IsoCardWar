from math import pi, sin
from typing import List, Tuple

import pygame

from common import SETTINGS_REF, Action, ActionArgs
from layer1 import (
    ParticleType,
    TerrainEnum,
    Tile,
    get_spawn_static_particle_action,
)
from layer2 import UIElementComponent


def get_toggle_menu_visibility(
    menus: List[UIElementComponent], menu_num: int
) -> Action:
    def toggle_menu_vis(_: ActionArgs = None) -> None:
        assert menu_num >= 0 and menu_num < len(menus)
        menus[menu_num].is_visible = not menus[menu_num].is_visible

    func = toggle_menu_vis
    return func


def get_spawn_dots_between_coords_action(
    pos_a: Tuple[int, int],
    pos_b: Tuple[int, int],
    arch: float,
    height: int,
    cnt: int,
) -> Action:
    def action(ent: ActionArgs) -> None:
        a_x, a_y = pos_a
        b_x, b_y = pos_b

        start_x, start_y = Tile(a_x, a_y, TerrainEnum.EMPTY).offset
        end_x, end_y = Tile(b_x, b_y, TerrainEnum.EMPTY).offset
        w = SETTINGS_REF.ISO_TILE_OFFSET_X
        h = SETTINGS_REF.ISO_TILE_OFFSET_Y * 3 - height
        start_x += w
        start_y += h
        end_x += w
        end_y += h

        def lerp(
            a: Tuple[float, float], b: Tuple[float, float], t: float
        ) -> Tuple[float, float]:
            ax, ay = a
            bx, by = b
            return (
                ax * t + bx * (1 - t),
                ay * t + by * (1 - t) - sin(pi * t) * arch,
            )

        for i in range(cnt):
            t = i / (cnt - 1)
            get_spawn_static_particle_action(
                t=ParticleType.CIRCLE,
                col=pygame.Color(255, 0, 0),
                pos=lerp((start_x, start_y), (end_x, end_y), t),
                size=3,
            )(None)

    return action
