from math import cos, pi, sin
from random import random
from typing import Tuple

import esper
import pygame

from common.dying import Health
from common.state import Action, ActionArgs

from .particles import PARTICLE_PROC_REF, Particle, ParticleType


def get_spawn_static_particle_action(
    t: ParticleType, col: pygame.Color, pos: Tuple[float, float], size: int
) -> Action:
    def action(ent: ActionArgs) -> None:
        p = Particle(
            particle_type=t, color=col, position=pos, size=size, immortal=True
        )
        h = Health()
        esper.create_entity(h, p)

    return action


def get_random_spawn_particle_action(
    t: ParticleType,
    col: pygame.Color,
    random_range: float,
    pos: Tuple[float, float],
    drag: float,
    mass: float,
    time: int,
    particle_count: int,
) -> Action:
    def action(_: ActionArgs) -> None:
        for _ in range(particle_count):
            theta = random() * pi * 2
            x = cos(theta) * random_range
            y = sin(theta) * random_range

            p = Particle(
                particle_type=t,
                color=col,
                velocity=(x, y),
                position=pos,
                drag=drag,
                immortal=False,
                size_by_hp=True,
                mass=mass,
                size=2,
            )
            h = Health(time)
            esper.create_entity(h, p)

    return action


def clear_particles_action(_: ActionArgs) -> None:
    PARTICLE_PROC_REF().clear_particles()
