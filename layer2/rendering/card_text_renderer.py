from typing import Type

import esper
import pygame

from common import BoundingBox, PositionTracker
from layer1.cards import deck_obj

from .card_renderer import CardSprite


class CardTextRenderer:
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

        ent_list = sorted(
            self.postrack.intersect(self.bb), key=lambda ent: sorter(ent), reverse=False
        )
        for ent in ent_list:
            sprite = esper.try_component(ent, CardSprite)

            if sprite is None:
                continue
            if deck_obj.hand.index(ent) != 2:
                continue

            sprite.mask.invert()
            i = deck_obj.hand.index(ent)
            for j in range(i + 1, len(deck_obj.hand)):
                prev_card_sprite = esper.component_for_entity(
                    deck_obj.hand[j], CardSprite
                )

                sprite.mask.draw(
                    prev_card_sprite.mask,
                    (
                        prev_card_sprite.rect.left - sprite.rect.left,
                        prev_card_sprite.rect.top - sprite.rect.top,
                    ),
                )
