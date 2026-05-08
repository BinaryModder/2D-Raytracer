from .vector2d import Vector2D


class Ray:
    def __init__(self, origin: Vector2D, direction: Vector2D):
        self.origin = origin
        self.direction = direction.normalize()
