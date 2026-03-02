from math import cos, pi, sin
from random import random
from typing import Tuple

import esper
import pygame

from common import Action, ActionDecor, ActionEnt, Health

from .particle_generator import ParticleGenerator
from .particles import PARTICLE_PROC_REF, Particle, ParticleType


def get_spawn_static_particle_action(
    t: ParticleType,
    col: pygame.Color,
    alpha: float,
    pos: Tuple[float, float],
    size: int,
) -> Action:
    @ActionDecor
    def action(ent: ActionEnt) -> bool:
        if ent is None or not esper.has_component(ent, ParticleGenerator):
            generator = ParticleGenerator()
        else:
            generator = esper.component_for_entity(ent, ParticleGenerator)
        p = Particle(
            particle_type=t,
            color=col,
            position=pos,
            size=size,
            immortal=True,
            alpha=alpha,
        )
        generator.add_particle(p)
        return True

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
    @ActionDecor
    def action(ent: ActionEnt) -> bool:
        if ent is None or not esper.has_component(ent, ParticleGenerator):
            generator = ParticleGenerator()
        else:
            generator = esper.component_for_entity(ent, ParticleGenerator)
        for _ in range(particle_count):
            theta = random() * pi * 2
            x = cos(theta) * random_range
            y = sin(theta) * random_range

            p = Particle(
                particle_type=t,
                color=pygame.Color(col),
                velocity=(x, y),
                position=pos,
                drag=drag,
                immortal=False,
                size_by_hp=True,
                mass=mass,
                size=2,
            )
            h = Health(time)
            generator.add_particle(p, h)
        return True

    return action


@ActionDecor
def clear_particles_action(ent: ActionEnt) -> bool:
    if ent is None or not esper.has_component(ent, ParticleGenerator):
        return True
    generator = esper.component_for_entity(ent, ParticleGenerator)
    generator.clear_particles()
    return True


@ActionDecor
def clear_all_particles_action(_: ActionEnt) -> bool:
    PARTICLE_PROC_REF().clear_particles()
    return True
