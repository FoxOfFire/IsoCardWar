from dataclasses import dataclass
from typing import Dict, Optional

import esper

from common import Health

from .particles import Particle


@dataclass
class ParticleGenerator:
    tracked_particles: Optional[Dict[int, Particle]] = None

    def add_particle(
        self, p: Particle, health: Optional[Health] = None
    ) -> None:
        if self.tracked_particles is None:
            self.tracked_particles = {}

        for part in self.tracked_particles.values():
            if part == p:
                return
        if health is None:
            health = Health()
        ent = esper.create_entity(p, health)

        self.tracked_particles.update({ent: p})

    def clear_particles(self) -> None:
        if self.tracked_particles is None:
            self.tracked_particles = {}

        for ent in self.tracked_particles:
            if esper.entity_exists(ent):
                esper.component_for_entity(ent, Particle).alpha = 0
        self.tracked_particles = {}
