from typing import Any, Tuple

import esper
import pygame

from common import BoundingBox, PositionTracker
from layer1.cards import deck_obj, play_card
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
            if tag.click_func is not None:
                tag.click_func(self.clicked, mouse_bb.center)
            if self.clicked in deck_obj.hand:
                play_card(self.clicked)
            self.clicked = -1

        # reset the hovering status of all entities from the previous frame
        for ent, tag in esper.get_component(UIElementComponent):
            if ent == self.clicked:
                continue
            if ent in self.tracker.intersect(mouse_bb) or tag.is_active:
                tag.state = UIStateEnum.HOVER
            else:
                tag.state = UIStateEnum.BASE

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

            comp: Any
            bit = 1
            for comp in esper.components_for_entity(ent):
                if not isinstance(comp, MaskedSprite):
                    continue
                if not comp.rect.collidepoint(mouse_bb.left, mouse_bb.top):
                    continue
                bit = comp.mask.get_at(
                    (mouse_bb.left - comp.rect.left, mouse_bb.top - comp.rect.top)
                )
            if bit == 0:
                continue

            if left_clicked:
                ui_tag.state = UIStateEnum.PRESSED
                self.clicked = ent
            else:
                ui_tag.state = UIStateEnum.HOVER
            break
