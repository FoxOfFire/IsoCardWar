from typing import Optional

import esper

from common import (
    RUN_DATA_REF,
    SETTINGS_REF,
    STATE_REF,
    BoundingBox,
)

from .cards import DECK_REF, Card
from .log import logger


class CardMovementProcessor(esper.Processor):
    cam_bb: Optional[BoundingBox] = None

    def set_cam_bb(self, bb: BoundingBox) -> None:
        self.cam_bb = bb
        logger.info("card cam set to:" + str(bb.points))

    def process(self) -> None:
        assert self.cam_bb is not None
        if len(DECK_REF.hand) == 0:
            return
        delta_time = RUN_DATA_REF.delta_time

        for ent, _ in esper.get_component(Card):
            bb = esper.component_for_entity(ent, BoundingBox)

            offset_index = DECK_REF.get_card_center_offset(ent)
            offset = (
                offset_index * self.cam_bb.width / len(DECK_REF.hand) * 0.8
            )
            if len(DECK_REF.hand) < 7:
                offset = offset_index * SETTINGS_REF.CARD_X_FIX_DISTANCE

            y = SETTINGS_REF.CARD_Y_POS_BASE
            if ent == STATE_REF.selected:
                y += SETTINGS_REF.CARD_Y_POS_SELECTED
            elif ent == STATE_REF.selecting:
                y += SETTINGS_REF.CARD_Y_POS_SELECTING

            delta_y = (
                (y - bb.center[1])
                / SETTINGS_REF.CARD_ANIMATION_SPEED
                * delta_time
            )
            delta_x = (
                (self.cam_bb.center[0] - bb.center[0] - (offset))
                / SETTINGS_REF.CARD_ANIMATION_SPEED
                * delta_time
            )
            bb.set_velocity(delta_x, delta_y)


CARD_MOV_PROC_REF = CardMovementProcessor()
