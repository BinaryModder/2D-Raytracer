import math


class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def cross(self, other):
        return self.x * other.y - self.y * other.x

    def normalize(self):
        mag = math.sqrt(self.x**2 + self.y**2)
        if mag == 0:
            return Vector2D(0, 0)
        return Vector2D(self.x / mag, self.y / mag)

    def __repr__(self):
        return f"V({self.x:.2f}, {self.y:.2f})"


class Ray:
    def __init__(self, origin: Vector2D, direction: Vector2D):
        self.origin = origin
        self.direction = direction.normalize()


class Segment:
    def __init__(self, p1: Vector2D, p2: Vector2D):
        self.p1 = p1
        self.p2 = p2

    def get_normal(self):
        wall_vec = self.p2 - self.p1
        return Vector2D(-wall_vec.y, wall_vec.x).normalize()


def get_intersection(ray: Ray, segment: Segment):
    d = ray.direction
    s = segment.p2 - segment.p1
    w = segment.p1 - ray.origin

    cross_d_s = d.cross(s)

    if abs(cross_d_s) < 1e-6:
        return None

    t = w.cross(s) / cross_d_s
    u = w.cross(d) / cross_d_s

    if t > 1e-4 and 0 <= u <= 1:
        intersection_point = ray.origin + d * t
        return intersection_point, t

    return None
