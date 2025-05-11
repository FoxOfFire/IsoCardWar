from typing import Set, Tuple

import esper
import pygame

from common import (
    BoundingBox,
    GameCamera,
    PositionTracker,
    UIElementComponent,
    UIStateEnum,
)

from .log import logger


class UIProcessor(esper.Processor):
    mousepos: Tuple[int, int]
    tracker: PositionTracker
    cam_bb: BoundingBox
    hovering: Set[int]
    clicked: Set[int]
    prev_click: bool
    world: str

    def __init__(self, ui_tracker: PositionTracker) -> None:
        self.world = esper.current_world
        cam_bb = BoundingBox(0, 1, 0, 1)
        for ent, bb in esper.get_component(BoundingBox):
            if esper.has_component(ent, GameCamera):
                cam_bb = bb
        self.tracker = ui_tracker
        self.cam_bb = cam_bb
        self.clicked = set()
        logger.info("init finished")
        self.prev_click = False

    def process(self) -> None:
        self.mousepos = pygame.mouse.get_pos()
        mouse_bb = BoundingBox(
            self.mousepos[0] - 1,
            self.mousepos[0] + 1,
            self.mousepos[1] - 1,
            self.mousepos[1] + 1,
        )
        (left_clicked, middle_clicked, right_clicked) = pygame.mouse.get_pressed()

        # this is nessecarry so that putton presses are not processed multiple times
        # reset the clicked status of all entitys from the previous frame
        click_buffer: Set[int] = set()
        if left_clicked:
            for ent in self.clicked:
                if ent in self.tracker.intersect(mouse_bb):
                    click_buffer.add(ent)
                else:
                    esper.component_for_entity(ent, UIElementComponent).state = (
                        UIStateEnum.BASE
                    )
        else:
            # handling button actions on release
            for ent in self.clicked:
                tag = esper.component_for_entity(ent, UIElementComponent)
                if tag.click_func is not None:
                    tag.click_func(ent)

        self.clicked = click_buffer

        # reset the hovering status of all entitys from the previous frame

        for ent, tag in esper.get_component(UIElementComponent):
            if ent in self.clicked:
                continue
            if ent in self.tracker.intersect(mouse_bb) or tag.is_active:
                tag.state = UIStateEnum.HOVER
            else:
                tag.state = UIStateEnum.BASE

        # check if mouse is over each item
        if self.prev_click and left_clicked:
            return
        self.prev_click = left_clicked

        for ent in self.tracker.intersect(mouse_bb):
            if not esper.has_component(ent, UIElementComponent) or (
                (ent in self.clicked)
            ):
                continue

            tag = esper.component_for_entity(ent, UIElementComponent)
            if not tag.is_visible or not tag.is_clickable:
                continue

            if left_clicked:

                tag.state = UIStateEnum.PRESSED
                self.clicked.add(ent)
                # logger.info(f"clicked: {ent}")
            else:
                tag.state = UIStateEnum.HOVER
            break
