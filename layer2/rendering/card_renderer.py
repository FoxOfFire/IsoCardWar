from typing import Type

import esper
import pygame

from common import BoundingBox, PositionTracker
from layer1.cards import CARD_HEIGHT, CARD_WIDTH, Card, deck_obj, get_card_angle
from layer2 import CardSprite

from .rendering_images import (
    CARD_IMAGES,
    CARD_MARKERS,
    CARD_TYPES,
    CardImageEnum,
    CardTypeEnum,
)

MARKER_X = 2
MARKER_Y = 2


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
            card = esper.try_component(ent, Card)
            if sprite is None or card is None:
                continue

            bb = esper.component_for_entity(ent, BoundingBox)
            surf = pygame.Surface((CARD_WIDTH, CARD_HEIGHT), flags=pygame.SRCALPHA)
            marker_surf = CARD_MARKERS[card.marker]

            surf.blit(CARD_IMAGES[CardImageEnum.BASIC][0], surf.get_rect())
            surf.blit(CARD_TYPES[CardTypeEnum.BASIC], surf.get_rect())
            surf.blit(marker_surf, marker_surf.get_rect(topleft=(MARKER_X, MARKER_Y)))

            rotated_surf = pygame.transform.rotate(surf, get_card_angle(ent))
            sprite.mask_offset = rotated_surf.get_rect().topleft
            sprite.mask = pygame.mask.from_surface(rotated_surf)

            sprite.rect = rotated_surf.get_rect(center=bb.center)
            screen.blit(rotated_surf, sprite.rect)
