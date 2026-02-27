from typing import Optional, Type

import esper
import pygame

from common import POS_PROC_REF, STATE_REF, BoundingBox, PriceEnum
from layer1 import DECK_REF, Card
from layer2.tags import MaskedSprite

from .asset_container_card import CARD_ASSET_REF
from .rendering_asset_loader import RENDER_ASSET_REF
from .utils import CardImageEnum, CardTypeEnum


class CardRenderer:
    bb: Optional[BoundingBox]

    def set_camera_type(self, cam_tag: Type) -> None:
        self.bb = esper.component_for_entity(
            esper.get_component(cam_tag)[0][0],
            BoundingBox,
        )

    def __init__(self) -> None:
        super().__init__()
        self.bb = None

    def draw(self, screen: pygame.Surface) -> None:
        assert self.bb is not None

        def sorter(ent: int) -> int:
            card = esper.try_component(ent, Card)
            if card is None or card not in DECK_REF.hand:
                return -1
            if ent == STATE_REF.selected_card:
                return 10000
            if ent == STATE_REF.hovered_ent:
                return 10001
            return DECK_REF.hand.index(card)

        def filterer(ent: int) -> bool:
            if not esper.entity_exists(ent):
                return False
            card = esper.try_component(ent, Card)
            return (
                card is not None
                and card in DECK_REF.hand
                and esper.has_component(ent, MaskedSprite)
            )

        ent_list = sorted(
            filter(filterer, POS_PROC_REF().intersect(self.bb)),
            key=sorter,
        )

        for ent in ent_list:
            assert esper.entity_exists(ent)

            sprite = esper.try_component(ent, MaskedSprite)
            card = esper.try_component(ent, Card)
            if sprite is None or card is None:
                continue

            bb = esper.component_for_entity(ent, BoundingBox)
            prices = []
            for res in PriceEnum:
                prices.append(card.price[res])
            mana, herbs, blood, brew = tuple(prices)
            surf = CARD_ASSET_REF.get_card_surf(
                border=CardTypeEnum.BASIC,
                image=CardImageEnum.BASIC_IMAGE,
                prices=(mana, herbs, blood, brew),
                frame=0,
            ).copy()
            RENDER_ASSET_REF.draw_text_on_surf(surf, ent)

            sprite.mask = pygame.mask.from_surface(surf)

            sprite.rect = surf.get_rect(center=bb.center)
            screen.blit(surf, sprite.rect)
