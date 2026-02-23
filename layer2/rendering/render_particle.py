from typing import Optional, Type

import esper
import pygame

from common import (
    BoundingBox,
    Health,
    Particle,
)

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

    def _get_circle_surf(
        self, particle: Particle, size: int
    ) -> pygame.Surface:
        surf = pygame.Surface((max(1, size), max(1, size)))
        surf.fill(particle.color)
        return surf

    def draw(self, screen: pygame.Surface) -> None:
        if self.bb is None:
            return

        for ent, particle in esper.get_component(Particle):

            if particle.size_by_hp:
                size = esper.component_for_entity(ent, Health).hp // 16
            else:
                x, y = particle.velocity
                size = x ^ 2 + y ^ 2

            surf = self._get_circle_surf(particle, size)

            screen.blit(surf, surf.get_rect(center=particle.position))
