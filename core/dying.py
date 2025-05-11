import esper

from common import Health
from common.position_tracking.position_tracker import PositionTracker


class DyingProcessor(esper.Processor):
    __game_tracker: PositionTracker

    def __init__(self, game_tracker: PositionTracker) -> None:
        self.__game_tracker = game_tracker

    def process(self) -> None:
        deleted: set = set()
        for ent, hp in esper.get_component(Health):
            if hp.hp <= 0:
                deleted.add(ent)
                self.__game_tracker.untrack(ent)
                esper.delete_entity(ent)
