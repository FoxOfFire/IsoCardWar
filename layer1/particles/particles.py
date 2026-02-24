from dataclasses import dataclass
from enum import IntEnum, auto
from math import atan2, cos, sin, sqrt
from typing import Dict, Tuple

import esper
import pygame

from common import (
    RUN_DATA_REF,
    WORLD_REF,
    Health,
    WorldEnum,
)


class ParticleType(IntEnum):
    CIRCLE = auto()


@dataclass
class Particle:
    particle_type: ParticleType
    color: pygame.Color
    position: Tuple[float, float]
    velocity: Tuple[float, float] = (0, 0)
    drag: float = 0
    mass: float = 2
    size: int = 5
    immortal: bool = False
    size_by_hp: bool = True

    def apply_velocity(self) -> None:
        x, y = self.position
        vel_x, vel_y = self.velocity
        d_t = RUN_DATA_REF.delta_time / 1000
        vel_x *= d_t
        vel_y *= d_t
        self.position = (x + vel_x, y + vel_y)

    def apply_drag(self) -> None:
        d_t = RUN_DATA_REF.delta_time / 1000
        vel_x, vel_y = self.velocity
        vel_pow = sqrt(pow(vel_x, 2) + pow(vel_y, 2))
        theta = atan2(vel_y, vel_x)
        drag = self.drag / self.mass * d_t

        drag_x = abs(cos(theta) * drag * vel_pow)
        drag_y = abs(sin(theta) * drag * vel_pow)

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
        for _, (particle, health) in esper.get_components(Particle, Health):
            particle.apply_drag()
            particle.apply_velocity()
            health.hp -= 1
            x, y = particle.position
            if abs(x) + abs(y) > 100000:
                health.hp = 0

    def clear_particles(self) -> None:
        for _, (_, health) in esper.get_components(Particle, Health):
            health.hp = 0


_POS_PROC_WORLD_DICT: Dict[WorldEnum, ParticleProcessor] = {}
for world in WorldEnum:
    _POS_PROC_WORLD_DICT.update({world: ParticleProcessor()})


def PARTICLE_PROC_REF() -> ParticleProcessor:
    return _POS_PROC_WORLD_DICT[WORLD_REF.world]
