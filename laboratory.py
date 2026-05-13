import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from math_engine import Vector2D, Ray, Segment, get_intersection, get_reflection


class RayTracingLab:

    def __init__(self, root):
        self.root = root
        self.root.title("Мини-лаборатория: 2D Ray Tracing")

        self.width = 600
        self.height = 400

        self.room_points = []
        self.ray_start = None
        self.ray_end = None
        self.mode = "DRAW_ROOM"

        self.main_container = tk.Frame(root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(self.main_container, width=self.width,
                                height=self.height, bg='#f0f0f0', cursor="crosshair")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        btn_frame = tk.Frame(self.main_container)
        btn_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(15, 0), anchor='n')

        button_width = 20

        self.btn_close = tk.Button(btn_frame, text="Замкнуть контур", command=self.close_room,
                                   state=tk.DISABLED, width=button_width)
        self.btn_close.grid(row=0, column=0, pady=5)

        self.btn_ray = tk.Button(btn_frame, text="Указать луч",
                                 state=tk.DISABLED, width=button_width)
        self.btn_ray.grid(row=1, column=0, pady=5)

        self.btn_run = tk.Button(btn_frame, text="Рассчитать", command=self.run_simulation,
                                 state=tk.DISABLED, bg='lightblue', width=button_width)
        self.btn_run.grid(row=2, column=0, pady=5)

        self.btn_clear = tk.Button(btn_frame, text="Очистить всё", command=self.clear_all,
                                   width=button_width)
        self.btn_clear.grid(row=3, column=0, pady=5)

        self.temp_ray_line = None

    def on_click(self, event):
        if self.mode == "DRAW_ROOM":
            pt = Vector2D(event.x, self.height - event.y)
            self.room_points.append(pt)

            r = 3
            self.canvas.create_oval(
                event.x-r, event.y-r, event.x+r, event.y+r, fill='black')

            if len(self.room_points) > 1:
                prev_x = self.room_points[-2].x
                prev_y = self.height - self.room_points[-2].y
                self.canvas.create_line(
                    prev_x, prev_y, event.x, event.y, width=2)

            if len(self.room_points) >= 3:
                self.btn_close.config(state=tk.NORMAL)

        elif self.mode == "DRAW_RAY":
            self.ray_start = Vector2D(event.x, self.height - event.y)

    def on_drag(self, event):
        if self.mode == "DRAW_RAY" and self.ray_start:
            if self.temp_ray_line:
                self.canvas.delete(self.temp_ray_line)
            start_x = self.ray_start.x
            start_y = self.height - self.ray_start.y
            self.temp_ray_line = self.canvas.create_line(
                start_x, start_y, event.x, event.y, fill='red', arrow=tk.LAST)

    def on_release(self, event):
        if self.mode == "DRAW_RAY" and self.ray_start:
            self.ray_end = Vector2D(event.x, self.height - event.y)
            self.mode = "DONE"
            self.btn_run.config(state=tk.NORMAL)

    def close_room(self):
        if len(self.room_points) >= 3:
            start_x = self.room_points[0].x
            start_y = self.height - self.room_points[0].y
            end_x = self.room_points[-1].x
            end_y = self.height - self.room_points[-1].y
            self.canvas.create_line(end_x, end_y, start_x, start_y, width=2)

            self.mode = "DRAW_RAY"
            self.btn_close.config(state=tk.DISABLED)
            self.btn_ray.config(state=tk.NORMAL)

    def clear_all(self):
        self.canvas.delete("all")
        self.room_points = []
        self.ray_start = None
        self.ray_end = None
        self.mode = "DRAW_ROOM"
        self.btn_close.config(state=tk.DISABLED)
        self.btn_run.config(state=tk.DISABLED)
        self.btn_ray.config(state=tk.DISABLED)

    def run_simulation(self):
        if len(self.room_points) < 3 or not self.ray_start or not self.ray_end:
            messagebox.showwarning(
                "Ошибка", "Сначала нарисуйте комнату и укажите луч!")
            return

        walls = []
        for i in range(len(self.room_points)):
            p1 = self.room_points[i]
            p2 = self.room_points[(i + 1) % len(self.room_points)]
            walls.append(Segment(p1, p2))

        direction = self.ray_end - self.ray_start
        if direction.x == 0 and direction.y == 0:
            messagebox.showwarning("Ошибка", "Вектор луча слишком короткий!")
            return

        current_ray = Ray(self.ray_start, direction)

        trajectory_x = [current_ray.origin.x]
        trajectory_y = [current_ray.origin.y]

        max_bounces = 30

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
        room_x = [p.x for p in self.room_points] + [self.room_points[0].x]
        room_y = [p.y for p in self.room_points] + [self.room_points[0].y]

        plt.plot(room_x, room_y, 'k-', linewidth=3, label="Контур")
        plt.plot(trajectory_x, trajectory_y, 'r-',
                 linewidth=1.5, alpha=0.8, label="Траектория")
        plt.scatter(trajectory_x, trajectory_y, color='blue', s=20, zorder=5)
        plt.scatter(trajectory_x[0], trajectory_y[0],
                    color='green', s=60, label="Старт", zorder=6)

        plt.title("Результат симуляции: Matplotlib")
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend()
        plt.axis('equal')
        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = RayTracingLab(root)
    root.mainloop()
