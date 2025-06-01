from typing import Type

import esper
import pygame

from common import BoundingBox, PositionTracker
from layer1 import game_state_obj
from layer1.cards import deck_obj

from .renderer_card import CardSprite


class MaskRenderer:
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
        selection_list = []
        if game_state_obj.selected is not None:
            selection_list.append(game_state_obj.selected)
            if ent_list.count(game_state_obj.selected) > 0:
                ent_list.remove(game_state_obj.selected)
        if game_state_obj.selecting is not None:
            selection_list.append(game_state_obj.selecting)
            if ent_list.count(game_state_obj.selecting) > 0:
                ent_list.remove(game_state_obj.selecting)

        for ent in ent_list:
            sprite = esper.try_component(ent, CardSprite)

            if sprite is None:
                continue

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

        for ent in selection_list:
            sprite = esper.try_component(ent, CardSprite)

            if sprite is None:
                continue

            for hand_ent in range(0, len(deck_obj.hand)):
                if ent == game_state_obj.selected or ent == game_state_obj.selecting:
                    continue
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

        for ent in ent_list:
            sprite = esper.try_component(ent, CardSprite)
            if sprite is None:
                continue
            sprite.mask.invert()

        if game_state_obj.selecting is not None and game_state_obj.selected is not None:
            selecting_sprite = esper.try_component(game_state_obj.selecting, CardSprite)
            selected_sprite = esper.try_component(game_state_obj.selected, CardSprite)
            if selecting_sprite is not None and selected_sprite is not None:

                selected_sprite.mask.invert()
                selected_sprite.mask.draw(
                    selecting_sprite.mask,
                    (
                        selecting_sprite.rect.left - selected_sprite.rect.left,
                        selecting_sprite.rect.top - selected_sprite.rect.top,
                    ),
                )
                selected_sprite.mask.invert()
