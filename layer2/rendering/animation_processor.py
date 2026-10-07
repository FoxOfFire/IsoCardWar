import esper

from common import RUN_DATA_REF, SETTINGS_REF


class AnimationInfoObject(esper.Processor):
    _animation_frame = 0
    _elapsed_time = 0

    def __init__(self) -> None:
        self._animation_frame = 0

    def get_frame_number(
        self, anim_length: int, *, start_offset: int = 0
    ) -> int:
        if anim_length < 2:
            return 0
        return (self._animation_frame + start_offset) % anim_length

    def process(self) -> None:
        self._elapsed_time += RUN_DATA_REF.delta_time
        if self._elapsed_time > SETTINGS_REF.ANIMATION_SPEED:
            self._elapsed_time -= SETTINGS_REF.ANIMATION_SPEED
            self._animation_frame += 1


ANIMATION_PROC_REF = AnimationInfoObject()
