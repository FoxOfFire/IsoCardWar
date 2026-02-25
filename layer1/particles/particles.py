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

    @property
    def velocity_x(self) -> float:
        return self.velocity[0]

    @property
    def velocity_y(self) -> float:
        return self.velocity[1]

    @property
    def position_x(self) -> float:
        return self.position[0]

    @property
    def position_y(self) -> float:
        return self.position[1]

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

        if vel_x > 0:
            drag_x = -drag_x
        if vel_y > 0:
            drag_y = -drag_y

        self.add_velocity((drag_x, drag_y))

    def add_velocity(self, velocity: Tuple[float, float]) -> None:
        x, y = velocity
        self.velocity = (self.velocity_x + x, self.velocity_y + y)

    def set_velocity(self, velocity: Tuple[float, float]) -> None:
        self.velocity = (0, 0)
        self.add_velocity(velocity)

    def add_position(self, position: Tuple[float, float]) -> None:
        x, y = position
        self.position = (self.position_x + x, self.position_y + y)

    def set_position(self, position: Tuple[float, float]) -> None:
        self.position = (0, 0)
        self.add_position(position)


class ParticleProcessor(esper.Processor):
    def process(self) -> None:
        for _, (particle, health) in esper.get_components(Particle, Health):
            particle.apply_drag()
            particle.apply_velocity()
            if not particle.immortal:
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
