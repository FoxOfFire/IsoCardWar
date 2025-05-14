from dataclasses import dataclass
from typing import Type

import esper
import pygame

from common import BoundingBox, PositionTracker
from layer1.cards import CARD_HEIGHT, CARD_WIDTH, deck_obj, get_card_angle

from .rendering_images import CARD_IMAGES, CARD_TYPES, CardImageEnum, CardTypeEnum
from .rendering_utils import MaskedSprite


@dataclass
class CardSprite(MaskedSprite):
    pass


class CardRenderer:
    def __init__(self, postrack: PositionTracker, tag: Type) -> None:
        super().__init__()
        self.postrack = postrack
        self.bb = esper.component_for_entity(
            esper.get_component(tag)[0][0],
            BoundingBox,
        )

    def draw(self, screen: pygame.Surface) -> None:
        def sorter(ent: int) -> int:
            if ent not in deck_obj.hand:
                return -1
            return deck_obj.hand.index(ent)

        ent_list = sorted(self.postrack.intersect(self.bb), key=lambda ent: sorter(ent))
        for ent in ent_list:
            sprite = esper.try_component(ent, CardSprite)
            if sprite is None:
                continue

            bb = esper.component_for_entity(ent, BoundingBox)
            surf = pygame.Surface((CARD_WIDTH, CARD_HEIGHT), flags=pygame.SRCALPHA)

            surf.blit(CARD_IMAGES[CardImageEnum.BASIC][0], surf.get_rect())
            surf.blit(CARD_TYPES[CardTypeEnum.BASIC], surf.get_rect())

            rotated_surf = pygame.transform.rotate(surf, get_card_angle(ent))
            sprite.mask_offset = rotated_surf.get_rect().topleft
            sprite.mask = pygame.mask.from_surface(rotated_surf)

            sprite.rect = rotated_surf.get_rect(center=bb.center)
            screen.blit(rotated_surf, sprite.rect)
