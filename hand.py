import numpy as np

import tkinter as tk

hand_lengths = [150, 250]
origin_position = np.array([450., 0])
canvas_size = (900, 500)

# How often change position
update_timeout = 500
# Angular speed, limits maximum angle change per timeout
angular_delta = 10 * np.pi / 180


def coordinates2angles(x, y):
    return np.pi * x / canvas_size[0], np.pi * y / canvas_size[1]


def compute_positions(angles):
    positions = [origin_position]
    total_angle = 0
    for angle, length in zip(angles, hand_lengths):
        total_angle += angle
        positions.append(positions[-1] + length * np.array([np.cos(total_angle), np.sin(total_angle)]))
    return positions


class Hand(object):
    def __init__(self, canvas: tk.Canvas, *args, **kwargs):
        self.canvas = canvas
        self.desired_angles = np.pi * np.ones_like(origin_position) / 2
        self.angles = np.zeros_like(origin_position)
        self.lines = [canvas.create_line(*origin_position, *(origin_position + 10), *args, **kwargs)
                      for _ in hand_lengths]

        self.canvas.after(update_timeout, self.update)

    def update(self):
        if not np.allclose(self.desired_angles, self.angles):
            self.angles += np.clip(self.desired_angles - self.angles, -angular_delta, angular_delta)

            positions = compute_positions(self.angles)
            print(*positions)
            for line, p1, p2 in zip(self.lines, positions[:-1], positions[1:]):
                self.canvas.coords(line, *p1, *p2)

        self.canvas.after(update_timeout, self.update)


class App:
    def __init__(self, master, **kwargs):
        self.master = master
        self.canvas = tk.Canvas(self.master, width=canvas_size[0], height=canvas_size[1])
        self.robot = Hand(self.canvas, fill='black', width=10)
        self.canvas.pack(fill=tk.BOTH)

        self.master.bind("<Button 1>", self.change_hand_position)

    def change_hand_position(self, event):
        x = float(event.x)
        y = float(event.y)
        angles = coordinates2angles(x, y)
        print(x, y, '\n', angles)

        self.robot.desired_angles = np.array(angles, dtype=float)

root = tk.Tk()
app = App(root)
root.mainloop()
