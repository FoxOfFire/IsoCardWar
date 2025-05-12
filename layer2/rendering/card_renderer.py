from dataclasses import dataclass

import esper
import pygame

from common import BoundingBox, PositionTracker
from layer1.cards import CARD_HEIGHT, CARD_WIDTH, deck_obj, get_card_center_offset
from layer2 import GameCameraTag

from .image_loader import CARD_IMAGES, CARD_TYPES, CardImageEnum, CardTypeEnum


@dataclass
class CardSprite:
    angle: float = 3


class CardRenderer:
    def __init__(self, postrack: PositionTracker) -> None:
        super().__init__()
        self.postrack = postrack
        self.bb = esper.component_for_entity(
            esper.get_component(GameCameraTag)[0][0],
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

            sprite.angle = get_card_center_offset(ent) * 4

            bb = esper.component_for_entity(ent, BoundingBox)
            surf = pygame.Surface((CARD_WIDTH, CARD_HEIGHT), flags=pygame.SRCALPHA)

            surf.blit(CARD_IMAGES[CardImageEnum.BASIC][0], surf.get_rect())
            surf.blit(CARD_TYPES[CardTypeEnum.BASIC], surf.get_rect())

            rotated_surf = pygame.transform.rotate(surf, sprite.angle)
            screen.blit(rotated_surf, rotated_surf.get_rect(center=bb.center))
