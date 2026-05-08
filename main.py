
import matplotlib.pyplot as plt
from math_engine import Vector2D, Ray, Segment, get_intersection, get_reflection


def create_room():
    points = [
        Vector2D(0, 0), Vector2D(10, 0),
        Vector2D(12, 5), Vector2D(8, 10),
        Vector2D(2, 8), Vector2D(0, 0)
    ]

    segments = []
    for i in range(len(points) - 1):
        segments.append(Segment(points[i], points[i+1]))
    return points, segments


def main():
    room_points, walls = create_room()

    current_ray = Ray(Vector2D(5, 2), Vector2D(1, 1.5))

    trajectory_x = [current_ray.origin.x]
    trajectory_y = [current_ray.origin.y]

    max_bounces = 20

    for _ in range(max_bounces):
        closest_intersection = None
        min_distance = float('inf')
        hit_wall = None

        for wall in walls:
            result = get_intersection(current_ray, wall)
            if result:
                intersection_point, distance = result
                if distance < min_distance:
                    min_distance = distance
                    closest_intersection = intersection_point
                    hit_wall = wall

        if not closest_intersection:
            break

        trajectory_x.append(closest_intersection.x)
        trajectory_y.append(closest_intersection.y)

        wall_normal = hit_wall.get_normal()

        if current_ray.direction.dot(wall_normal) > 0:
            wall_normal = wall_normal * -1

        new_direction = get_reflection(current_ray.direction, wall_normal)

        current_ray = Ray(closest_intersection, new_direction)

    plt.figure(figsize=(8, 6))

    room_x = [p.x for p in room_points]
    room_y = [p.y for p in room_points]
    plt.plot(room_x, room_y, 'k-', linewidth=3, label="Стены")

    plt.plot(trajectory_x, trajectory_y, 'r-', linewidth=1.5,
             alpha=0.8, label="Траектория луча")
    plt.scatter(trajectory_x, trajectory_y, color='blue', s=20, zorder=5)
    plt.scatter(trajectory_x[0], trajectory_y[0],
                color='green', s=60, label="Старт", zorder=6)

    plt.title("Симуляция 2D Ray Tracing (Математический бильярд)")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.axis('equal')
    plt.show()


if __name__ == "__main__":
    main()
