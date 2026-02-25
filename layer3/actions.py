from typing import Tuple

import pygame

from common import SETTINGS_REF, Action, ActionArgs, add2i, lerp2
from layer1 import (
    ParticleType,
    TerrainEnum,
    Tile,
    get_spawn_static_particle_action,
)


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

        start = Tile(a_x, a_y, TerrainEnum.EMPTY).offset
        end = Tile(b_x, b_y, TerrainEnum.EMPTY).offset
        w = SETTINGS_REF.ISO_TILE_OFFSET_X
        h = SETTINGS_REF.ISO_TILE_OFFSET_Y * 3 - height
        start = add2i(start, (w, h))
        end = add2i(end, (w, h))

        for i in range(cnt):
            t = i / (cnt - 1)
            get_spawn_static_particle_action(
                t=ParticleType.CIRCLE,
                col=pygame.Color(255, 0, 0),
                pos=lerp2(start, end, t),
                size=3,
            )(None)

    return action
