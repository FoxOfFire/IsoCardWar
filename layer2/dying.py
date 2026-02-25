import esper

from common import POS_PROC_REF, BoundingBox, Health


class DyingProcessor(esper.Processor):

    def process(self) -> None:
        for ent, hp in esper.get_component(Health):
            if hp.hp <= 0:
                if esper.has_component(ent, BoundingBox):
                    POS_PROC_REF().untrack(ent)
                esper.delete_entity(ent)


DYING_PROC_REF = DyingProcessor()
