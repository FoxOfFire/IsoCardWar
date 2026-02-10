from typing import List, Optional, Tuple, Type

import esper
import pygame

from common import POS_PROC_REF, SETTINGS_REF, STATE_REF, BoundingBox
from layer1 import DECK_REF

from .log import logger
from .renderer_card import CardSprite


class MaskRenderer:
    bb: Optional[BoundingBox]

    def set_camera_type(self, cam_tag: Type) -> None:
        logger.info("set cam type to:" + str(cam_tag))
        self.bb = esper.component_for_entity(
            esper.get_component(cam_tag)[0][0],
            BoundingBox,
        )

    def __init__(self, track_tag: Type) -> None:
        super().__init__()
        self.track_tag = track_tag
        self.bb = None

    def _get_sorted_hand_and_selection(self) -> Tuple[List[int], List[int]]:
        assert self.bb is not None

        def sorter(ent: int) -> int:
            if ent not in DECK_REF.hand:
                return -1
            return DECK_REF.hand.index(ent)

        ent_list = sorted(
            POS_PROC_REF.intersect(self.bb, self.track_tag),
            key=lambda ent: sorter(ent),
            reverse=False,
        )

        ent_list = list(
            filter(
                lambda ent: ent in DECK_REF.hand
                and esper.has_component(ent, CardSprite),
                ent_list,
            )
        )

        selection_list = []
        selected = STATE_REF.selected
        selecting = STATE_REF.selecting

        if selected is not None and selected in ent_list:
            ent_list.remove(selected)
            selection_list.append(selected)
        if selecting is not None and selecting in ent_list:
            ent_list.remove(selecting)
            selection_list.append(selecting)
        return ent_list, selection_list

    def _draw_hand_masks(self, ent_list: List[int]) -> None:
        for ent in ent_list:
            assert (
                esper.entity_exists(ent)
                and ent in DECK_REF.hand
                and esper.has_component(ent, CardSprite)
            )

            sprite = esper.component_for_entity(ent, CardSprite)
            sprite.mask.invert()
            this = DECK_REF.hand.index(ent)

            for next in range(this + 1, len(DECK_REF.hand)):
                ent = DECK_REF.hand[next]
                assert esper.entity_exists(ent)

                next_card_sprite = esper.component_for_entity(ent, CardSprite)

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
            assert esper.entity_exists(ent)

            sprite = esper.try_component(ent, CardSprite)
            assert sprite is not None

            for hand_ent in ent_list:
                assert esper.entity_exists(hand_ent)

                hand_sprite = esper.try_component(hand_ent, CardSprite)
                assert hand_sprite is not None

                hand_sprite.mask.draw(
                    sprite.mask,
                    (
                        sprite.rect.left - hand_sprite.rect.left,
                        sprite.rect.top - hand_sprite.rect.top,
                    ),
                )

    def _invert_hand(self, ent_list: List[int]) -> None:
        for ent in ent_list:
            assert esper.entity_exists(ent)

            sprite = esper.try_component(ent, CardSprite)
            assert sprite is not None

            sprite.mask.invert()

    def _draw_selection_to_selected(self) -> None:
        if STATE_REF.selecting is None or STATE_REF.selected is None:
            return

        assert esper.entity_exists(STATE_REF.selected) and esper.entity_exists(
            STATE_REF.selecting
        )

        selecting_sprite = esper.try_component(STATE_REF.selecting, CardSprite)
        selected_sprite = esper.try_component(STATE_REF.selected, CardSprite)

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

    def _draw_mask_on_screen(
        self, screen: pygame.Surface, ent_list: List[int]
    ) -> None:
        for ent in ent_list:
            assert esper.entity_exists(ent)

            sprite = esper.try_component(ent, CardSprite)
            assert sprite is not None

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
        if SETTINGS_REF.RENDER_MASKS:
            self._draw_mask_on_screen(screen, ent_list + selection_list)
