from typing import Any, List, Optional, Tuple, Type

import esper
import pygame

from common import (
    COLOR_REF,
    POS_PROC_REF,
    SETTINGS_REF,
    STATE_REF,
    BoundingBox,
)
from layer1 import DECK_REF, Card, Tile
from layer2.tags import MaskedSprite

from .log import logger


class MaskRenderer:
    bb: Optional[BoundingBox]

    def set_camera_type(self, cam_tag: Type) -> None:
        logger.info("set cam type to:" + str(cam_tag))
        self.bb = esper.component_for_entity(
            esper.get_component(cam_tag)[0][0],
            BoundingBox,
        )

    def __init__(self, track_ui: Type, track_iso: Type) -> None:
        super().__init__()
        self.track_ui = track_ui
        self.track_iso = track_iso
        self.bb = None

    def _get_masked_sprite(self, ent: int) -> Optional[MaskedSprite]:
        comp: Any
        for comp in esper.components_for_entity(ent):
            if isinstance(comp, MaskedSprite):
                return comp
        return None

    def _has_masked_sprite(self, ent: int) -> bool:
        return self._get_masked_sprite(ent) is not None

    def _get_sorted_hand_and_selection(self) -> Tuple[List[int], List[int]]:
        assert self.bb is not None

        def sorter(ent: int) -> int:
            card = esper.try_component(ent, Card)
            if card is not None and card in DECK_REF.hand:
                return DECK_REF.hand.index(card)
            return -1

        def filterer(ent: int) -> bool:
            return (
                esper.entity_exists(ent)
                and self._has_masked_sprite(ent)
                and (
                    esper.has_component(ent, Card)
                    or esper.has_component(ent, Tile)
                )
            )

        ent_list = POS_PROC_REF().intersect(self.bb, self.track_ui)
        ent_list += POS_PROC_REF().intersect(self.bb, self.track_iso)
        ent_list = sorted(filter(filterer, ent_list), key=sorter)

        selection_list = []

        for ent in ent_list:
            if ent == STATE_REF.selected_card or ent == STATE_REF.hovered_ent:
                selection_list.append(ent)

        for ent in selection_list:
            ent_list.remove(ent)

        return ent_list, selection_list

    def _draw_hand_masks(self, ent_list: List[int]) -> None:
        for ent in ent_list:
            card = esper.try_component(ent, Card)
            if card is None:
                continue
            sprite = self._get_masked_sprite(ent)
            if sprite is None:
                continue
            sprite.mask.invert()
            this = ent_list.index(ent)

            for next_ent in range(this + 1, len(ent_list)):
                ent = ent_list[next_ent]
                assert esper.entity_exists(ent)

                next_card_sprite = self._get_masked_sprite(ent)
                if next_card_sprite is None:
                    continue
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

            sprite = self._get_masked_sprite(ent)
            assert sprite is not None

            for hand_ent in ent_list:
                assert esper.entity_exists(hand_ent)

                hand_sprite = self._get_masked_sprite(hand_ent)
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

            sprite = self._get_masked_sprite(ent)
            assert sprite is not None

            sprite.mask.invert()

    def _draw_selection_to_selected(self) -> None:
        if STATE_REF.hovered_ent is None or STATE_REF.selected_card is None:
            return

        assert esper.entity_exists(
            STATE_REF.selected_card
        ) and esper.entity_exists(STATE_REF.hovered_ent)

        hovered_sprite = self._get_masked_sprite(STATE_REF.hovered_ent)
        selected_sprite = self._get_masked_sprite(STATE_REF.selected_card)

        if hovered_sprite is None or selected_sprite is None:
            return

        selected_sprite.mask.invert()
        selected_sprite.mask.draw(
            hovered_sprite.mask,
            (
                hovered_sprite.rect.left - selected_sprite.rect.left,
                hovered_sprite.rect.top - selected_sprite.rect.top,
            ),
        )
        selected_sprite.mask.invert()

    def _draw_mask_on_screen(
        self, screen: pygame.Surface, ent_list: List[int]
    ) -> None:
        db_white = pygame.Color(COLOR_REF.WHITE)
        db_white.a = 50
        db_black = pygame.Color(COLOR_REF.BLACK)
        db_black.a = 50

        for ent in ent_list:
            assert esper.entity_exists(ent)

            sprite = self._get_masked_sprite(ent)
            assert sprite is not None

            screen.blit(
                sprite.mask.to_surface(setcolor=db_white, unsetcolor=db_black),
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
