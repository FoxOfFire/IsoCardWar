from typing import List, Optional

import esper

from common import Health

from .particles import Particle


class ParticleGenerator:
    tracked_particles: List[int] = []

    def add_particle(
        self, p: Particle, health: Optional[Health] = None
    ) -> None:
        if health is None:
            health = Health()
        ent = esper.create_entity(p, health)
        self.tracked_particles.append(ent)

    def clear_particles(self) -> None:
        for ent in self.tracked_particles:
            if not esper.entity_exists(ent) or not esper.has_component(
                ent, Health
            ):
                continue
            esper.component_for_entity(ent, Health).hp = 0
        self.tracked_particles = []
