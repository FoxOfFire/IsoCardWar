from typing import List, Tuple, Type

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

    def _get_sorted_hand_and_selection(self) -> Tuple[List[int], List[int]]:
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
        selected = game_state_obj.selected
        selecting = game_state_obj.selecting
        if selected is not None and selected in ent_list:
            ent_list.remove(selected)
            selection_list.append(selected)
        if selecting is not None and selecting in ent_list:
            ent_list.remove(selecting)
            selection_list.append(selecting)
        return ent_list, selection_list

    def _draw_hand_masks(self, ent_list: List[int]) -> None:
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

    def _draw_selection_to_hand(
        self, ent_list: List[int], selection_list: List[int]
    ) -> None:
        for ent in selection_list:
            sprite = esper.try_component(ent, CardSprite)
            if sprite is None:
                continue
            for hand_ent in ent_list:
                hand_sprite = esper.try_component(hand_ent, CardSprite)
                if hand_sprite is None:
                    continue

                hand_sprite.mask.draw(
                    sprite.mask,
                    (
                        sprite.rect.left - hand_sprite.rect.left,
                        sprite.rect.top - hand_sprite.rect.top,
                    ),
                )

    def _invert_hand(self, ent_list: List[int]) -> None:
        for ent in ent_list:
            sprite = esper.try_component(ent, CardSprite)
            if sprite is None:
                continue
            sprite.mask.invert()

    def _draw_selection_to_selected(self) -> None:
        if game_state_obj.selecting is None or game_state_obj.selected is None:
            return
        selecting_sprite = esper.try_component(game_state_obj.selecting, CardSprite)
        selected_sprite = esper.try_component(game_state_obj.selected, CardSprite)
        if selecting_sprite is None or selected_sprite is None:
            return

        selected_sprite.mask.invert()
        selected_sprite.mask.draw(
            selecting_sprite.mask,
            (
                selecting_sprite.rect.left - selected_sprite.rect.left,
                selecting_sprite.rect.top - selected_sprite.rect.top,
            ),
        )
        selected_sprite.mask.invert()

    def _draw_mask_on_screen(self, screen: pygame.Surface, ent_list: List[int]) -> None:
        for ent in ent_list:
            sprite = esper.try_component(ent, CardSprite)
            if sprite is None:
                continue
            screen.blit(
                sprite.mask.to_surface(
                    setcolor=pygame.Color(255, 255, 255, 50),
                    unsetcolor=pygame.Color(0, 0, 0, 50),
                ),
                sprite.rect,
            )

    def draw(self, screen: pygame.Surface) -> None:
        ent_list, selection_list = self._get_sorted_hand_and_selection()

        self._draw_hand_masks(ent_list)
        self._draw_selection_to_hand(ent_list, selection_list)
        self._invert_hand(ent_list)
        self._draw_selection_to_selected()
        # self._draw_mask_on_screen(screen, ent_list + selection_list)
