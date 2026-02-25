from functools import partial
from typing import Optional, Tuple

import esper
import pygame

from common import SETTINGS_REF, Action, ActionArgs, add2i, lerp1, lerp2
from layer1 import (
    MAP_DATA_REF,
    ParticleType,
    TerrainEnum,
    Tile,
    get_spawn_static_particle_action,
)


def get_spawn_dots_between_coords_action(
    pos_a: Tuple[int, int],
    pos_b: Tuple[int, int],
    *,
    arch: float,
    height: int,
    cnt: int,
    cutoff: int,
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
            alpha: float = 0
            t = i / (cnt - 1)
            col = pygame.Color(
                round(lerp1(200, 255, t)),
                round(lerp1(100, 30, t)),
                round(lerp1(10, 30, t)),
            )

            if i < cutoff:
                alpha += 1 - (i) / (cutoff)
            if i >= cnt - cutoff:
                alpha += (i + 1 - (cnt - cutoff)) / (cutoff)
            if alpha < 0.00001:
                continue

            get_spawn_static_particle_action(
                t=ParticleType.CIRCLE,
                col=col,
                alpha=alpha,
                pos=lerp2(start, end, t, arch=arch),
                size=2,
            )(ent)

    return action


def get_spawn_dots_between_ent_and_target(cutoff: Optional[int]) -> Action:

    def action(cut: Optional[int], ent: ActionArgs) -> None:
        if ent is None or not esper.has_component(ent, Tile):
            return
        tile = esper.component_for_entity(ent, Tile)
        if tile.target is None:
            return

        ent_pos = MAP_DATA_REF.pos_at(ent)
        ent_x, ent_y = ent_pos
        target_pos = MAP_DATA_REF.pos_at(tile.target)
        target_x, target_y = target_pos

        diff = max(abs(ent_x - target_x), abs(ent_y - target_y))
        diff = diff * 4 - 1

        if cut is None:
            cut = diff
        get_spawn_dots_between_coords_action(
            ent_pos, target_pos, arch=60, height=0, cnt=diff, cutoff=cut
        )(ent)

    return partial(action, cutoff)
