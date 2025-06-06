from dataclasses import dataclass
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
from layer1 import GAME_STATE_REF
from layer1.cards import DECK_REF, Card
from layer2 import MaskedSprite

from .rendering_asset_loader import (
    CARD_IMAGE_SURFS,
    CARD_MARKER_SURFS,
    CARD_TYPE_SURFS,
    CardImageEnum,
    CardTypeEnum,
)
from .utils import draw_text_on_surf


@dataclass
class CardSprite(MaskedSprite):
    pass


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
            if ent not in DECK_REF.hand:
                return -1
            if ent == GAME_STATE_REF.selected:
                return 10000
            if ent == GAME_STATE_REF.selecting:
                return 10001
            return DECK_REF.hand.index(ent)

        ent_list = sorted(
            self.pos_track.intersect(self.bb), key=lambda ent: sorter(ent)
        )
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
            draw_text_on_surf(surf, ent)

            sprite.mask = pygame.mask.from_surface(surf)

            sprite.rect = surf.get_rect(center=bb.center)
            screen.blit(surf, sprite.rect)
