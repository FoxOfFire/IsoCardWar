import esper

from common import BoundingBox
from common.constants import (
    CARD_ANIMATION_SPEED,
    CARD_ROTATION_PER_CARD,
    CARD_X_FIX_DISTANCE,
    CARD_Y_POS_BASE,
    CARD_Y_POS_SELECTED,
    CARD_Y_POS_SELECTING,
)
from layer1 import game_state_obj

from .cards import Card, deck_obj, get_card_center_offset


class CardMovementProcessor(esper.Processor):
    def __init__(self, cam_bb: BoundingBox) -> None:
        self.cam_bb = cam_bb

    def process(self) -> None:
        if len(deck_obj.hand) == 0:
            return

        for ent, card in esper.get_component(Card):
            bb = esper.component_for_entity(ent, BoundingBox)

            offset_index = get_card_center_offset(ent)
            offset = offset_index * self.cam_bb.width / len(deck_obj.hand) * 0.8
            if len(deck_obj.hand) < 7:
                offset = offset_index * CARD_X_FIX_DISTANCE

            y = CARD_Y_POS_BASE
            if ent == game_state_obj.selected:
                y += CARD_Y_POS_SELECTED
                target_angle = 0.0
            elif ent == game_state_obj.selecting:
                y += CARD_Y_POS_SELECTING
                target_angle = 0.0
            else:
                if card.target_angle is None:
                    target_angle = offset_index * CARD_ROTATION_PER_CARD
                else:
                    target_angle = card.target_angle

            delta_y = (y - bb.center[1]) / CARD_ANIMATION_SPEED
            delta_x = (
                self.cam_bb.center[0] - bb.center[0] - (offset)
            ) / CARD_ANIMATION_SPEED
            bb.move(delta_x, delta_y)

            delta_angle = (target_angle - card.current_angle) / CARD_ANIMATION_SPEED
            if abs(delta_angle) > 0.1:
                card.current_angle += delta_angle
            else:
                card.current_angle = target_angle
