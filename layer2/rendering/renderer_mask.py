from typing import List, Optional, Tuple, Type

import esper
import pygame

from common import (
    POS_PROC_REF,
    SETTINGS_REF,
    STATE_REF,
    BoundingBox,
    ColorEnum,
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
                and esper.has_component(ent, MaskedSprite)
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
            card = esper.try_component(ent, Card)
            sprite = esper.try_component(ent, MaskedSprite)
            if (
                esper.has_component(ent, Tile)
                or card is None
                or sprite is None
            ):
                continue

            sprite.mask.invert()
            this = ent_list.index(ent)

            for next_ent in range(this + 1, len(ent_list)):
                if esper.has_component(ent, Tile):
                    continue
                ent = ent_list[next_ent]

                next_card_sprite = esper.try_component(ent, MaskedSprite)
                if next_card_sprite is None:
                    continue
                self._draw_sprite_owerlap(sprite, next_card_sprite)

    def _draw_selection_to_hand(
        self, ent_list: List[int], selection_list: List[int]
    ) -> None:
        for ent in selection_list:
            if esper.has_component(ent, Tile):
                continue

            sprite = esper.component_for_entity(ent, MaskedSprite)

            for hand_ent in ent_list:
                if esper.has_component(ent, Tile):
                    continue

                hand_sprite = esper.component_for_entity(
                    hand_ent, MaskedSprite
                )

                self._draw_sprite_owerlap(hand_sprite, sprite)

    def _invert_hand(self, ent_list: List[int]) -> None:
        for ent in ent_list:
            if esper.has_component(ent, Tile):
                continue

            sprite = esper.component_for_entity(ent, MaskedSprite)
            sprite.mask.invert()

    def _draw_selection_to_selected(self) -> None:
        hover = STATE_REF.hovered_ent
        select = STATE_REF.selected_card
        if hover is None or select is None:
            return

        hovered_sprite = esper.try_component(hover, MaskedSprite)
        selected_sprite = esper.try_component(select, MaskedSprite)
        if hovered_sprite is None or selected_sprite is None:
            return

        self._draw_sprite_owerlap(selected_sprite, hovered_sprite, invert=True)

    def _draw_mask_on_screen(
        self, screen: pygame.Surface, ent_list: List[int]
    ) -> None:
        mask_surf = pygame.mask.Mask(screen.get_size())
        mask_surf.fill()

        for ent in ent_list:
            sprite = esper.component_for_entity(ent, MaskedSprite)

            screen.blit(
                sprite.mask.to_surface(
                    setcolor=ColorEnum.MASK_SET.value,
                    unsetcolor=ColorEnum.MASK_UNSET.value,
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
