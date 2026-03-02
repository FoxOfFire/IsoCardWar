from typing import Optional, Tuple

import esper

from common import (
    SETTINGS_REF,
    Action,
    ActionDecor,
    ActionEnt,
    ColorEnum,
    add2i,
    lerp2,
)
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
    @ActionDecor
    def action(ent: ActionEnt) -> bool:
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
            col = ColorEnum.RED.value
            if i < cutoff:
                alpha += 1 - (i) / (cutoff)
            if i >= cnt - cutoff:
                alpha += (i + 1 - (cnt - cutoff)) / (cutoff)
            if alpha < 0.00001:
                continue

            if not get_spawn_static_particle_action(
                t=ParticleType.CIRCLE,
                col=col,
                alpha=alpha,
                pos=lerp2(start, end, t, arch=arch),
                size=2,
            )(ent, True):
                return False
        return True

    return action


def get_spawn_dots_between_ent_and_target(cutoff: Optional[int]) -> Action:

    @ActionDecor
    def action(ent: ActionEnt) -> bool:
        if ent is None or not esper.has_component(ent, Tile):
            return False
        tile = esper.component_for_entity(ent, Tile)
        if tile.target is None:
            return False

        ent_pos = MAP_DATA_REF.pos_at(ent)
        ent_x, ent_y = ent_pos
        target_pos = MAP_DATA_REF.pos_at(tile.target)
        target_x, target_y = target_pos

        diff = max(abs(ent_x - target_x), abs(ent_y - target_y))
        diff = diff * 4 - 1

        if cutoff is None:
            cut = diff
        else:
            cut = cutoff
        return get_spawn_dots_between_coords_action(
            ent_pos,
            target_pos,
            arch=60,
            height=0,
            cnt=max(diff, 8),
            cutoff=cut,
        )(ent, True)

    return action
