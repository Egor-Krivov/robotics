import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scene import Disturber, Drone, Scene
from utils import flatten, create_trajectory

low = 0
high = 10
n_frames = 1000
points_initial = 11
np.random.seed(21)


def render():
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                         xlim=(low, high), ylim=(low, high))
    ax.grid()

    line_dis, = ax.plot([], [], '-', lw=2)
    pos_dis, = ax.plot([], [], 'o', lw=3, c='b')
    line_drone_list = [ax.plot([], [], 'x', markersize=8, lw=3, c='b')[0] for _ in swarm]

    def init():
        """initialize animation"""
        line_dis.set_data([], [])
        for elem in line_drone_list:
            elem.set_data([], [])
        pos_dis.set_data([], [])
        output = tuple(flatten([line_dis, line_drone_list, pos_dis]))
        return output

    def animate(i):
        swarm_position = [drone.current_pos for drone in scene.drones]
        disturber_position = trajectory[i, :]
        scene.update_scene(swarm_position, disturber_position)

        line_dis.set_data(trajectory[:i, :].T)
        pos_dis.set_data(disturber_position)
        [line_drone_list[num].set_data(drone.current_pos) for num, drone in enumerate(scene.drones)]
        output = tuple(flatten([line_dis, line_drone_list, pos_dis]))
        return output

    _ = animation.FuncAnimation(fig, animate, frames=n_frames,
                                  interval=10, blit=True, init_func=init)

    plt.show()


trajectory = create_trajectory(low, high, points_initial, points_generated=n_frames)

swarm = (Drone(initial_pos=np.array([2, 5]), drone_id=1), Drone(initial_pos=np.array([4, 5]), drone_id=2), Drone(initial_pos=np.array([7, 7]), drone_id=3),
         Drone(initial_pos=np.array([6, 5]), drone_id=4), Drone(initial_pos=np.array([8, 1]), drone_id=5), Drone(initial_pos=np.array([8, 8]), drone_id=6),
         Drone(initial_pos=np.array([1, 8]), drone_id=1))
disturber = Disturber(initial_pos=trajectory[0, :])
scene = Scene(disturber, swarm)

render()

