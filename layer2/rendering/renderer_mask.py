from typing import List, Tuple, Type

import esper
import pygame

from common import BoundingBox
from common.constants import RENDER_MASKS
from layer1 import GAME_STATE_REF
from layer1.cards import DECK_REF

from .renderer_card import CardSprite


class MaskRenderer:
    def __init__(self, cam_tag: Type, track_tag: Type) -> None:
        super().__init__()
        self.track_tag = track_tag
        self.bb = esper.component_for_entity(
            esper.get_component(cam_tag)[0][0],
            BoundingBox,
        )

    def _get_sorted_hand_and_selection(self) -> Tuple[List[int], List[int]]:
        ent_list = DECK_REF.hand.copy()

        selection_list = []
        selected = GAME_STATE_REF.selected
        selecting = GAME_STATE_REF.selecting

        if selected is not None and selected in ent_list:
            ent_list.remove(selected)
            selection_list.append(selected)
        if selecting is not None and selecting in ent_list:
            ent_list.remove(selecting)
            selection_list.append(selecting)
        return ent_list, selection_list

    def _draw_hand_masks(self, ent_list: List[int]) -> None:
        for ent in ent_list:
            if (
                not esper.entity_exists(ent)
                or ent not in DECK_REF.hand
                or not esper.has_component(ent, CardSprite)
            ):
                continue

            sprite = esper.component_for_entity(ent, CardSprite)
            sprite.mask.invert()
            this = DECK_REF.hand.index(ent)

            for next in range(this + 1, len(DECK_REF.hand)):

                next_card_sprite = esper.component_for_entity(
                    DECK_REF.hand[next], CardSprite
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
            if not esper.entity_exists(ent):
                continue

            sprite = esper.try_component(ent, CardSprite)
            if sprite is None:
                continue
            for hand_ent in ent_list:
                if not esper.entity_exists(hand_ent):
                    continue

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
            if not esper.entity_exists(ent):
                continue

            sprite = esper.try_component(ent, CardSprite)
            if sprite is None:
                continue
            sprite.mask.invert()

    def _draw_selection_to_selected(self) -> None:
        if GAME_STATE_REF.selecting is None or GAME_STATE_REF.selected is None:
            return
        if not esper.entity_exists(GAME_STATE_REF.selected) or not esper.entity_exists(
            GAME_STATE_REF.selecting
        ):
            return
        selecting_sprite = esper.try_component(GAME_STATE_REF.selecting, CardSprite)
        selected_sprite = esper.try_component(GAME_STATE_REF.selected, CardSprite)
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
            if not esper.entity_exists(ent):
                continue

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
        if RENDER_MASKS:
            self._draw_mask_on_screen(screen, ent_list + selection_list)
