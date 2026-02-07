from typing import Any, Tuple

import esper
import pygame

from common import GAME_CAM_HEIGHT, GAME_CAM_WIDTH, POS_PROC_REF, BoundingBox
from layer1 import GAME_STATE_REF, GamePhaseEnum
from layer2.tags import (
    GameCameraTag,
    MaskedSprite,
    UIElementComponent,
    UIStateEnum,
)

from .log import logger


class UIProcessor(esper.Processor):

    def __init__(self, display_size: Tuple[int, int]) -> None:
        for ent, bb in esper.get_component(BoundingBox):
            if esper.has_component(ent, GameCameraTag):
                self.cam_bb = bb
                break
        self.clicked: int = -1
        self.hover: int = -1
        logger.info("init finished")
        self.prev_click = False

        self.display_size = display_size

    def clicked_things_stay_clicked(self, mouse_bb: BoundingBox) -> int:
        click_buffer: int = -1
        if self.clicked == -1:
            return click_buffer

        ent = self.clicked
        if ent in POS_PROC_REF.intersect_ent_type(mouse_bb, ent):
            click_buffer = ent
        else:
            esper.component_for_entity(ent, UIElementComponent).state = (
                UIStateEnum.BASE
            )

        return click_buffer

    def mask_overlap(self, ent: int, bb: BoundingBox) -> bool:
        bit = 1
        assert esper.entity_exists(ent)
        comp: Any
        for comp in esper.components_for_entity(ent):
            if not isinstance(comp, MaskedSprite):
                continue
            bit = 0
            if comp.rect.collidepoint(bb.left, bb.top):
                bit = comp.mask.get_at(
                    (bb.left - comp.rect.left, bb.top - comp.rect.top)
                )
            break
        return bit == 1

    def process(self) -> None:
        self.mouse_pos = pygame.mouse.get_pos()
        mouse_bb = BoundingBox(
            self.mouse_pos[0] * (GAME_CAM_WIDTH / self.display_size[0]),
            self.mouse_pos[0] * (GAME_CAM_WIDTH / self.display_size[0]),
            self.mouse_pos[1] * (GAME_CAM_HEIGHT / self.display_size[1]),
            self.mouse_pos[1] * (GAME_CAM_HEIGHT / self.display_size[1]),
        )
        (left_clicked, _, _) = pygame.mouse.get_pressed()

        # things that wer clicked on previous frame stay clicked
        if left_clicked:
            self.clicked = self.clicked_things_stay_clicked(mouse_bb)
        # pressing the button on release
        if self.clicked != -1 and self.prev_click:
            tag = esper.component_for_entity(self.clicked, UIElementComponent)
            if (
                tag.click_func is not None
                and self.mask_overlap(self.clicked, mouse_bb)
                and (
                    GAME_STATE_REF.game_phase == GamePhaseEnum.PLAYER_ACTION
                    or not tag.is_gameplay_elem
                )
            ):
                tag.click_func(self.clicked, -1)
            self.clicked = -1

        # reset the hovering status of all entities from the previous frame
        unhovered: bool = False
        for ent, tag in esper.get_component(UIElementComponent):
            assert esper.entity_exists(ent)
            if ent == self.clicked:
                continue
            if (
                ent in POS_PROC_REF.intersect_ent_type(mouse_bb, ent)
                or tag.is_active
            ):
                tag.state = UIStateEnum.HOVER
            else:
                unhovered = unhovered or ent == self.hover
                tag.state = UIStateEnum.BASE
        if unhovered:
            tag = esper.component_for_entity(self.hover, UIElementComponent)
            if tag.unhover_func is not None:
                tag.unhover_func(self.hover, -1)

        # exiting clicking if continuing to click
        if self.prev_click and left_clicked:
            return
        self.prev_click = left_clicked

        # pressing first intersection of mouse
        for ent in POS_PROC_REF.intersect_ent_type(mouse_bb, ent):
            assert esper.entity_exists(ent)
            ui_tag = esper.try_component(ent, UIElementComponent)
            assert ui_tag is not None
            if (
                ent == self.clicked
                or not ui_tag.is_visible
                or not ui_tag.is_clickable
                or not self.mask_overlap(ent, mouse_bb)
            ):
                continue

            if left_clicked:
                ui_tag.state = UIStateEnum.PRESSED
                self.clicked = ent
            elif ui_tag.hover_func is not None:
                ui_tag.hover_func(ent, -1)
                ui_tag.state = UIStateEnum.HOVER
                self.hover = ent
            break
