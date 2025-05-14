import esper

from common import BoundingBox

from .card_utils import CARD_Y_POS
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
                offset = offset_index * 30

            delta_x = (
                self.cam_bb.center[0] - bb.center[0] - (offset)
            ) / card.anim_speed
            bb.delta_right = delta_x
            bb.delta_left = delta_x

            delta_y = (CARD_Y_POS - bb.center[1]) / card.anim_speed
            bb.delta_top = delta_y
            bb.delta_bottom = delta_y
            if card.target_angle is None:
                card.current_angle += (
                    offset_index * 4 - card.current_angle
                ) / card.anim_speed
            else:
                card.current_angle -= (
                    card.target_angle - card.current_angle
                ) / card.anim_speed
