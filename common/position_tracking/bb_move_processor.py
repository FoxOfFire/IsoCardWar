import esper

from common.position_tracking.bounding_box import BoundingBox

class BBMoveProcessor(esper.Processor):
    def process(self) -> None:
        for _, bb in esper.get_component(BoundingBox):
            if bb.has_nonzero_delta:
                bb.right += bb._delta_x
                bb.left += bb._delta_x
                bb.top += bb._delta_y
                bb.bottom += bb._delta_y
                bb._delta_x = 0
                bb._delta_y = 0
