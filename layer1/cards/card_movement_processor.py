import esper

from common import BoundingBox
from common.constants import (
    CARD_ANIMATION_SPEED,
    CARD_X_FIX_DISTANCE,
    CARD_Y_POS_BASE,
    CARD_Y_POS_SELECTED,
    CARD_Y_POS_SELECTING,
)
from common.globals import RUN_DATA_REF
from layer1 import GAME_STATE_REF

from .cards import DECK_REF, Card, get_card_center_offset


class CardMovementProcessor(esper.Processor):
    def __init__(self, cam_bb: BoundingBox) -> None:
        self.cam_bb = cam_bb

    def process(self) -> None:
        if len(DECK_REF.hand) == 0:
            return
        delta_time = RUN_DATA_REF.delta_time

        for ent, _ in esper.get_component(Card):
            bb = esper.component_for_entity(ent, BoundingBox)

            offset_index = get_card_center_offset(ent)
            offset = offset_index * self.cam_bb.width / len(DECK_REF.hand) * 0.8
            if len(DECK_REF.hand) < 7:
                offset = offset_index * CARD_X_FIX_DISTANCE

            y = CARD_Y_POS_BASE
            if ent == GAME_STATE_REF.selected:
                y += CARD_Y_POS_SELECTED
            elif ent == GAME_STATE_REF.selecting:
                y += CARD_Y_POS_SELECTING

            delta_y = (y - bb.center[1]) / CARD_ANIMATION_SPEED * delta_time
            delta_x = (
                (self.cam_bb.center[0] - bb.center[0] - (offset))
                / CARD_ANIMATION_SPEED
                * delta_time
            )
            bb.set_velocity(delta_x, delta_y)
