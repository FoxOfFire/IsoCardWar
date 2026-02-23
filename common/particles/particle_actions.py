from random import randint
from typing import Tuple

import esper
import pygame

from common.dying import Health
from common.state import Action, ActionArgs

from .particles import Particle, ParticleType


def get_random_spawn_particle_action(
    t: ParticleType,
    col: pygame.Color,
    random_range: int,
    pos: Tuple[int, int],
    drag: Tuple[int, int],
    time: int,
) -> Action:
    def action(_: ActionArgs) -> None:
        x = randint(-random_range, random_range)
        y = randint(-random_range, random_range)

        p = Particle(
            particle_type=t,
            color=col,
            velocity=(x, y),
            position=pos,
            drag=drag,
            immortal=False,
            size_by_hp=True,
        )
        h = Health(time)
        esper.create_entity(h, p)

    return action
