from dataclasses import dataclass
from enum import IntEnum, auto
from typing import Dict, Tuple

import esper
import pygame

from common.dying import Health
from common.worlds import WORLD_REF, WorldEnum


class ParticleType(IntEnum):
    CIRCLE = auto()


@dataclass
class Particle:
    particle_type: ParticleType
    color: pygame.Color
    position: Tuple[int, int]
    velocity: Tuple[int, int] = (0, 0)
    drag: Tuple[int, int] = (0, 0)
    immortal: bool = False
    size_by_hp: bool = True

    def apply_velocity(self) -> None:
        x, y = self.position
        vel_x, vel_y = self.velocity
        self.position = (x + vel_x, y + vel_y)

    def apply_drag(self) -> None:
        vel_x, vel_y = self.velocity
        drag_x, drag_y = self.drag

        if vel_x < 0:
            vel_x = min(0, vel_x + drag_x)
        else:
            vel_x = max(0, vel_x - drag_x)

        if vel_y < 0:
            vel_y = min(0, vel_y + drag_y)
        else:
            vel_y = max(0, vel_y - drag_y)

        self.velocity = (vel_x, vel_y)


class ParticleProcessor(esper.Processor):
    def process(self) -> None:
        for ent, particle in esper.get_component(Particle):
            particle.apply_velocity()
            particle.apply_drag()
            health = esper.component_for_entity(ent, Health)
            health.hp -= 1


_POS_PROC_WORLD_DICT: Dict[WorldEnum, ParticleProcessor] = {}
for world in WorldEnum:
    _POS_PROC_WORLD_DICT.update({world: ParticleProcessor()})


def PARTICLE_PROC_REF() -> ParticleProcessor:
    return _POS_PROC_WORLD_DICT[WORLD_REF.world]
