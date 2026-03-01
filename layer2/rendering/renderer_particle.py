from typing import Optional, Type

import esper
import pygame

from common import COLOR_REF, BoundingBox, lerp1
from layer1 import Particle, ParticleType

from .log import logger


class ParticleRenderer:
    bb: Optional[BoundingBox]
    surf: Optional[pygame.Surface]

    def set_camera_type(self, cam_tag: Type) -> None:
        cams = esper.get_component(cam_tag)
        if len(cams) > 0:
            self.bb = esper.component_for_entity(cams[0][0], BoundingBox)
            self.surf = pygame.Surface(
                (self.bb.width, self.bb.height), flags=pygame.SRCALPHA
            )

    def __init__(self) -> None:
        super().__init__()
        self.bb = None
        self.surf = None
        logger.info("iso renderer init finished")

    def _draw_circle_particle(
        self, particle: Particle, screen: pygame.Surface
    ) -> None:
        col = pygame.Color(particle.color)
        col.a = round(lerp1(0, 255, particle.alpha))
        pygame.draw.circle(screen, col, particle.position, particle.size)

    def draw(self, screen: pygame.Surface) -> None:
        if self.bb is None or self.surf is None:
            return
        self.surf.fill(COLOR_REF.TRANSPARENT)

        for _, particle in esper.get_component(Particle):
            match particle.particle_type:
                case ParticleType.CIRCLE:
                    self._draw_circle_particle(particle, self.surf)
                case _:
                    raise RuntimeError("Particle type rendering not specified")
        screen.blit(self.surf)
