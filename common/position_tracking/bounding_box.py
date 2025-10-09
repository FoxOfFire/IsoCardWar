from typing import Tuple


class BoundingBox:
    left: float = 0
    right: float = 0
    top: float = 0
    bottom: float = 0

    _delta_x: float = 0
    _delta_y:float = 0

    def __init__(self,left:float,right:float,top:float,bottom:float) -> None:
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
   
    @property
    def center(self) -> tuple[float, float]:
        return ((self.left + self.right) / 2, (self.top + self.bottom) / 2)

    @property
    def width(self) -> float:
        return self.right - self.left

    @property
    def height(self) -> float:
        return self.bottom-self.top 

    @property
    def points(self) -> tuple[float, float, float, float]:
        return(self.left,self.right,self.top,self.bottom)

    @property
    def has_nonzero_delta(self) -> bool:
        return self._delta_x+self._delta_y == self._delta_x-self._delta_y

    def move_by(self, delta_x: float, delta_y: float) -> None:
        self._delta_x += delta_x
        self._delta_y += delta_y

    def move_towards_point(
        self, point: tuple[float, float], by: float
    ) -> None:
        def lerp(a:float,b:float,t:float)->float:
            return t*a+(1-t)*b
        self._delta_x += lerp(self.center[0],point[0],by)
        self._delta_y += lerp(self.center[1],point[1],by)
