from typing import Any, Optional, Tuple

import esper
import pygame

from common import (
    GAME_STATE_REF,
    POS_PROC_REF,
    SETTINGS_REF,
    BoundingBox,
    GamePhaseEnum,
)
from layer2.tags import (
    GameCameraTag,
    MaskedSprite,
    UIElementComponent,
    UIStateEnum,
)

from .log import logger


class UIProcessor(esper.Processor):

    def __init__(self) -> None:
        for ent, bb in esper.get_component(BoundingBox):
            if esper.has_component(ent, GameCameraTag):
                self.cam_bb = bb
                break
        self.clicked: Optional[int] = None
        self.mouse_bb: Optional[BoundingBox] = None
        self.hover: Optional[int] = None
        logger.info("init finished")
        self.prev_click = False
        self.display_size: Optional[Tuple[int, int]] = None

    def set_display_size(self, display_size: Tuple[int, int]) -> None:
        logger.info("set display size:" + str(display_size))
        self.display_size = display_size

    def clicked_things_stay_clicked(self) -> None:
        assert self.mouse_bb is not None
        click_buffer: Optional[int] = None
        if self.clicked is None:
            self.clicked = click_buffer
            return

        ent = self.clicked
        if ent in POS_PROC_REF.intersect_ent_type(self.mouse_bb, ent):
            click_buffer = ent
        else:
            esper.component_for_entity(ent, UIElementComponent).state = (
                UIStateEnum.BASE
            )

        self.clicked = click_buffer

    def mask_mouse_overlap(self, ent: int) -> bool:
        bit = 1
        assert esper.entity_exists(ent)
        assert self.mouse_bb is not None
        comp: Any
        for comp in esper.components_for_entity(ent):
            if not isinstance(comp, MaskedSprite):
                continue
            bit = 0
            if comp.rect.collidepoint(self.mouse_bb.left, self.mouse_bb.top):
                bit = comp.mask.get_at(
                    (
                        self.mouse_bb.left - comp.rect.left,
                        self.mouse_bb.top - comp.rect.top,
                    )
                )
            break
        return bit == 1

    def press_button_on_release(self) -> None:
        assert self.mouse_bb is not None
        if self.clicked is not None and self.prev_click:
            tag = esper.component_for_entity(self.clicked, UIElementComponent)
            if self.mask_mouse_overlap(self.clicked) and (
                GAME_STATE_REF.game_phase == GamePhaseEnum.PLAYER_ACTION
                or not tag.is_gameplay_elem
            ):
                for func in tag.click_func:
                    func((self.clicked, None))
            self.clicked = None

        pass

    def get_and_reset_hovered_ent(self) -> int:
        assert self.mouse_bb is not None
        unhovered: bool = False
        for ent, tag in esper.get_component(UIElementComponent):
            assert esper.entity_exists(ent)
            if ent == self.clicked:
                continue
            if (
                ent in POS_PROC_REF.intersect_ent_type(self.mouse_bb, ent)
                or tag.is_active
            ):
                tag.state = UIStateEnum.HOVER
            else:
                unhovered = unhovered or ent != self.hover
                tag.state = UIStateEnum.BASE
            if unhovered and self.hover is not None:
                tag = esper.component_for_entity(
                    self.hover, UIElementComponent
                )
                for func in tag.unhover_func:
                    func((ent, None))
        return ent

    def process(self) -> None:
        assert self.display_size is not None
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_bb = BoundingBox(
            self.mouse_pos[0]
            * (SETTINGS_REF.GAME_CAM_WIDTH / self.display_size[0]),
            self.mouse_pos[0]
            * (SETTINGS_REF.GAME_CAM_WIDTH / self.display_size[0]),
            self.mouse_pos[1]
            * (SETTINGS_REF.GAME_CAM_HEIGHT / self.display_size[1]),
            self.mouse_pos[1]
            * (SETTINGS_REF.GAME_CAM_HEIGHT / self.display_size[1]),
        )
        left_clicking, _, _ = pygame.mouse.get_pressed()

        if left_clicking:
            self.clicked_things_stay_clicked()

        self.press_button_on_release()

        mouse_over_ent = self.get_and_reset_hovered_ent()

        # exiting clicking if continuing to click
        if self.prev_click and left_clicking:
            return
        self.prev_click = left_clicking

        # pressing first intersection of mouse
        for ent in POS_PROC_REF.intersect_ent_type(
            self.mouse_bb, mouse_over_ent
        ):
            assert esper.entity_exists(ent)
            ui_tag = esper.try_component(ent, UIElementComponent)
            assert ui_tag is not None
            if (
                ent == self.clicked
                or not ui_tag.is_visible
                or not ui_tag.is_clickable
                or not self.mask_mouse_overlap(ent)
            ):
                continue

            if left_clicking:
                ui_tag.state = UIStateEnum.PRESSED
                self.clicked = ent
            else:
                for func in ui_tag.hover_func:
                    func((ent, None))
                    ui_tag.state = UIStateEnum.HOVER
                    self.hover = ent
            break


UI_PROC_REF = UIProcessor()
