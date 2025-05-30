from typing import Type

import esper
import pygame

from common import BoundingBox, PositionTracker
from layer1.cards import deck_obj

from .card_renderer import CardSprite


class CardTextRenderer:
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
                return -1
            return deck_obj.hand.index(ent)

        ent_list = sorted(
            self.pos_track.intersect(self.bb),
            key=lambda ent: sorter(ent),
            reverse=False,
        )
        for ent in ent_list:
            sprite = esper.try_component(ent, CardSprite)

            if sprite is None:
                continue

            if ent == deck_obj.selected:
                for hand_ent in range(0, len(deck_obj.hand)):
                    hand_sprite = esper.component_for_entity(
                        deck_obj.hand[hand_ent], CardSprite
                    )
                    hand_sprite.mask.invert()
                    hand_sprite.mask.draw(
                        sprite.mask,
                        (
                            sprite.rect.left - hand_sprite.rect.left,
                            sprite.rect.top - hand_sprite.rect.top,
                        ),
                    )
                    hand_sprite.mask.invert()
            elif ent in deck_obj.hand:
                sprite.mask.invert()
                this = deck_obj.hand.index(ent)
                for next in range(this + 1, len(deck_obj.hand)):

                    next_card_sprite = esper.component_for_entity(
                        deck_obj.hand[next], CardSprite
                    )

                    sprite.mask.draw(
                        next_card_sprite.mask,
                        (
                            next_card_sprite.rect.left - sprite.rect.left,
                            next_card_sprite.rect.top - sprite.rect.top,
                        ),
                    )

        for ent in ent_list:
            sprite = esper.try_component(ent, CardSprite)
            if sprite is None:
                continue
            sprite.mask.invert()
