from dataclasses import dataclass
from typing import Optional, Type

import esper
import pygame

from common import (
    POS_PROC_REF,
    SETTINGS_REF,
    STATE_REF,
    BoundingBox,
)
from layer1 import DECK_REF, Card
from layer2.tags import MaskedSprite

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
    bb: Optional[BoundingBox]

    def set_camera_type(self, cam_tag: Type) -> None:
        self.bb = esper.component_for_entity(
            esper.get_component(cam_tag)[0][0],
            BoundingBox,
        )

    def __init__(self, track_tag: Type) -> None:
        super().__init__()
        self.track_tag = track_tag
        self.bb = None

    def draw(self, screen: pygame.Surface) -> None:
        assert self.bb is not None

        def sorter(ent: int) -> int:
            if ent not in DECK_REF.hand:
                return -1
            if ent == STATE_REF.selected_card:
                return 10000
            if ent == STATE_REF.hovered_ent:
                return 10001
            return DECK_REF.hand.index(ent)

        ent_list = sorted(
            POS_PROC_REF.intersect(self.bb, self.track_tag),
            key=lambda ent: sorter(ent),
        )

        for ent in ent_list:
            assert esper.entity_exists(ent)

            sprite = esper.try_component(ent, CardSprite)
            card = esper.try_component(ent, Card)
            if sprite is None or card is None:
                continue

            bb = esper.component_for_entity(ent, BoundingBox)
            surf = pygame.Surface(
                (SETTINGS_REF.CARD_WIDTH, SETTINGS_REF.CARD_HEIGHT),
                flags=pygame.SRCALPHA,
            )
            marker_surf = CARD_MARKER_SURFS[card.marker]

            surf.blit(
                CARD_IMAGE_SURFS[CardImageEnum.BASIC][0], surf.get_rect()
            )
            surf.blit(CARD_TYPE_SURFS[CardTypeEnum.BASIC], surf.get_rect())
            surf.blit(
                marker_surf,
                marker_surf.get_rect(
                    topleft=(
                        SETTINGS_REF.RELATIVE_MARKER_POS_X,
                        SETTINGS_REF.RELATIVE_MARKER_POS_Y,
                    )
                ),
            )
            draw_text_on_surf(surf, ent)

            sprite.mask = pygame.mask.from_surface(surf)

            sprite.rect = surf.get_rect(center=bb.center)
            screen.blit(surf, sprite.rect)
