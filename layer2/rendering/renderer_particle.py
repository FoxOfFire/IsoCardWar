from typing import Optional, Type

import esper
import pygame

from common import BoundingBox
from layer1 import Particle

from .log import logger


class ParticleRenderer:
    bb: Optional[BoundingBox]

    def set_camera_type(self, cam_tag: Type) -> None:
        cams = esper.get_component(cam_tag)
        if len(cams) > 0:
            self.bb = esper.component_for_entity(cams[0][0], BoundingBox)

    def __init__(self, track_tag: Type, /) -> None:
        super().__init__()
        self.track_tag = track_tag
        self.bb = None
        logger.info("iso renderer init finished")

    def _draw_circle_particle(
        self, particle: Particle, screen: pygame.Surface
    ) -> None:
        pygame.draw.circle(
            screen, particle.color, particle.position, particle.size
        )

    def draw(self, screen: pygame.Surface) -> None:
        if self.bb is None:
            return

        for _, particle in esper.get_component(Particle):
            self._draw_circle_particle(particle, screen)
