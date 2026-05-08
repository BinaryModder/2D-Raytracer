
from .vector2d import Vector2D


class Segment:
    def __init__(self, p1: Vector2D, p2: Vector2D):
        self.p1 = p1
        self.p2 = p2

    def get_normal(self):
        wall_vec = self.p2 - self.p1
        return Vector2D(-wall_vec.y, wall_vec.x).normalize()
