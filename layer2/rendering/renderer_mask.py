from typing import List, Optional, Tuple, Type

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

    def __init__(self) -> None:
        super().__init__()
        self.bb = None

    def _get_masked_sprite(self, ent: int) -> Optional[MaskedSprite]:
        return esper.try_component(ent, MaskedSprite)

    def _has_masked_sprite(self, ent: int) -> bool:
        return esper.has_component(ent, MaskedSprite)

    def _draw_sprite_owerlap(
        self,
        target: MaskedSprite,
        drawer: MaskedSprite,
        *,
        invert: bool = False,
        erase: bool = False
    ) -> None:
        if invert:
            target.mask.invert()
        if not erase:
            target.mask.draw(
                drawer.mask,
                (
                    drawer.rect.left - target.rect.left,
                    drawer.rect.top - target.rect.top,
                ),
            )
        else:
            target.mask.erase(
                drawer.mask,
                (
                    drawer.rect.left - target.rect.left,
                    drawer.rect.top - target.rect.top,
                ),
            )
        if invert:
            target.mask.invert()

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

        ent_list = POS_PROC_REF().intersect(self.bb)
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
            if esper.has_component(ent, Tile):
                continue
            card = esper.try_component(ent, Card)
            if card is None:
                continue
            sprite = self._get_masked_sprite(ent)
            if sprite is None:
                continue
            sprite.mask.invert()
            this = ent_list.index(ent)

            for next_ent in range(this + 1, len(ent_list)):
                if esper.has_component(ent, Tile):
                    continue
                ent = ent_list[next_ent]
                assert esper.entity_exists(ent)

                next_card_sprite = self._get_masked_sprite(ent)
                if next_card_sprite is None:
                    continue
                self._draw_sprite_owerlap(sprite, next_card_sprite)

    def _draw_selection_to_hand(
        self, ent_list: List[int], selection_list: List[int]
    ) -> None:
        for ent in selection_list:
            if esper.has_component(ent, Tile):
                continue
            assert esper.entity_exists(ent)

            sprite = self._get_masked_sprite(ent)
            assert sprite is not None

            for hand_ent in ent_list:
                if esper.has_component(ent, Tile):
                    continue
                assert esper.entity_exists(hand_ent)

                hand_sprite = self._get_masked_sprite(hand_ent)
                assert hand_sprite is not None

                self._draw_sprite_owerlap(hand_sprite, sprite)

    def _invert_hand(self, ent_list: List[int]) -> None:
        for ent in ent_list:
            assert esper.entity_exists(ent)
            if esper.has_component(ent, Tile):
                continue

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

        self._draw_sprite_owerlap(selected_sprite, hovered_sprite, invert=True)

    def _draw_mask_on_screen(
        self, screen: pygame.Surface, ent_list: List[int]
    ) -> None:
        mask_sprite = MaskedSprite()
        mask_surf = pygame.mask.Mask(screen.get_size())
        mask_surf.fill()
        mask_sprite.mask = mask_surf
        mask_sprite.rect = screen.get_rect()

        for ent in ent_list:
            sprite = self._get_masked_sprite(ent)

            assert sprite is not None
            screen.blit(
                sprite.mask.to_surface(
                    setcolor=COLOR_REF.MASK_SET, unsetcolor=COLOR_REF.MASK_UNSET
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
