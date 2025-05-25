from typing import Any, Tuple

import esper
import pygame

from common import BoundingBox, PositionTracker
from layer2.tags import GameCameraTag, MaskedSprite, UIElementComponent, UIStateEnum

from .log import logger


class UIProcessor(esper.Processor):

    def __init__(
        self, ui_tracker: PositionTracker, display_size: Tuple[int, int]
    ) -> None:
        for ent, bb in esper.get_component(BoundingBox):
            if esper.has_component(ent, GameCameraTag):
                self.cam_bb = bb
                break
        self.tracker = ui_tracker
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

        if ent in self.tracker.intersect(mouse_bb):
            click_buffer = ent
        else:
            esper.component_for_entity(ent, UIElementComponent).state = UIStateEnum.BASE

        return click_buffer

    def mask_overlap(self, ent: int, bb: BoundingBox) -> bool:
        bit = 1
        comp: Any
        for comp in esper.components_for_entity(ent):
            if not isinstance(comp, MaskedSprite):
                continue
            bit = 0
            if comp.rect.collidepoint(bb.left, bb.top):
                bit = comp.mask.get_at(
                    (bb.left - comp.rect.left, bb.top - comp.rect.top)
                )
        return bit == 1

    def process(self) -> None:
        self.mouse_pos = pygame.mouse.get_pos()
        mouse_bb = BoundingBox(
            self.mouse_pos[0] * (self.cam_bb.width / self.display_size[0]),
            self.mouse_pos[0] * (self.cam_bb.width / self.display_size[0]),
            self.mouse_pos[1] * (self.cam_bb.height / self.display_size[1]),
            self.mouse_pos[1] * (self.cam_bb.height / self.display_size[1]),
        )
        (left_clicked, _, _) = pygame.mouse.get_pressed()

        # things that wer clicked on previous frame stay clicked
        if left_clicked:
            self.clicked = self.clicked_things_stay_clicked(mouse_bb)
        # pressing the button on release
        elif self.clicked != -1 and self.prev_click:
            tag = esper.component_for_entity(self.clicked, UIElementComponent)
            if tag.click_func is not None and self.mask_overlap(self.clicked, mouse_bb):
                tag.click_func(self.clicked)
            self.clicked = -1

        # reset the hovering status of all entities from the previous frame
        unhovered: bool = False
        for ent, tag in esper.get_component(UIElementComponent):
            if ent == self.clicked:
                continue
            if ent in self.tracker.intersect(mouse_bb) or tag.is_active:
                tag.state = UIStateEnum.HOVER
            else:
                unhovered = unhovered or ent == self.hover
                tag.state = UIStateEnum.BASE
        if unhovered:
            tag = esper.component_for_entity(self.hover, UIElementComponent)
            if tag.unhover_func is not None:
                tag.unhover_func(self.hover)

        # exiting clicking if continuing to click
        if self.prev_click and left_clicked:
            return
        self.prev_click = left_clicked

        # pressing first intersection of mouse
        for ent in self.tracker.intersect(mouse_bb):
            ui_tag = esper.try_component(ent, UIElementComponent)
            if ent == self.clicked or (
                ui_tag is None or not ui_tag.is_visible or not ui_tag.is_clickable
            ):
                continue
            if not self.mask_overlap(ent, mouse_bb):
                continue

            if left_clicked:
                ui_tag.state = UIStateEnum.PRESSED
                self.clicked = ent
            else:
                if ui_tag.hover_func is not None:
                    ui_tag.hover_func(ent)
                ui_tag.state = UIStateEnum.HOVER
                self.hover = ent
            break
