
from classes import Ray, Segment, Vector2D


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


def get_reflection(incident_vector: Vector2D, normal_vector: Vector2D):
    dot_product = incident_vector.dot(normal_vector)

    reflection_x = incident_vector.x - 2 * dot_product * normal_vector.x
    reflection_y = incident_vector.y - 2 * dot_product * normal_vector.y

    return Vector2D(reflection_x, reflection_y).normalize()
