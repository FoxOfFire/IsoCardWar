from typing import Type

import esper
import pygame

from common import BoundingBox, PositionTracker
from common.constants import (
    CARD_HEIGHT,
    CARD_WIDTH,
    RELATIVE_MARKER_POS_X,
    RELATIVE_MARKER_POS_Y,
)
from layer1 import game_state_obj
from layer1.cards import Card, deck_obj, get_card_angle
from layer2 import CardSprite

from .rendering_images import (
    CARD_IMAGE_SURFS,
    CARD_MARKER_SURFS,
    CARD_TYPE_SURFS,
    CardImageEnum,
    CardTypeEnum,
)


class CardRenderer:
    def __init__(self, pos_track: PositionTracker, tag: Type) -> None:
        super().__init__()
        self.pos_track = pos_track
        self.bb = esper.component_for_entity(
            esper.get_component(tag)[0][0],
            BoundingBox,
        )

    def draw(self, screen: pygame.Surface) -> None:
        def sorter(ent: int) -> int:
            if ent not in deck_obj.hand:
                return 1000
            return deck_obj.hand.index(ent)

        ent_list = sorted(
            self.pos_track.intersect(self.bb), key=lambda ent: sorter(ent)
        )
        if game_state_obj.selected is not None:
            ent_list.append(game_state_obj.selected)
        for ent in ent_list:
            sprite = esper.try_component(ent, CardSprite)
            card = esper.try_component(ent, Card)
            if sprite is None or card is None:
                continue

            bb = esper.component_for_entity(ent, BoundingBox)
            surf = pygame.Surface((CARD_WIDTH, CARD_HEIGHT), flags=pygame.SRCALPHA)
            marker_surf = CARD_MARKER_SURFS[card.marker]

            surf.blit(CARD_IMAGE_SURFS[CardImageEnum.BASIC][0], surf.get_rect())
            surf.blit(CARD_TYPE_SURFS[CardTypeEnum.BASIC], surf.get_rect())
            surf.blit(
                marker_surf,
                marker_surf.get_rect(
                    topleft=(RELATIVE_MARKER_POS_X, RELATIVE_MARKER_POS_Y)
                ),
            )

            rotated_surf = pygame.transform.rotate(surf, get_card_angle(ent))
            sprite.mask = pygame.mask.from_surface(rotated_surf)

            sprite.rect = rotated_surf.get_rect(center=bb.center)
            screen.blit(rotated_surf, sprite.rect)
