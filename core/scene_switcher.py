import esper


class ScenceSwitcher(esper.Processor):
    next_tick_world: str | None

    def __init__(self) -> None:
        self.next_tick_world = None

    def process(self) -> None:
        if (
            self.next_tick_world is not None
            and esper.current_world != self.next_tick_world
        ):
            esper.switch_world(self.next_tick_world)
            self.next_tick_world = None
