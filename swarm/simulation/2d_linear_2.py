import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
from scipy.interpolate import interp1d
from sklearn.preprocessing import normalize

lim = np.array([0, 10])
n_frames = 1000
np.random.seed(42)


def create_random_trajectory(points_initial=7, points_generated=n_frames):
    x = np.linspace(*lim, num=points_initial)
    y = np.random.uniform(low=lim[0] + 0.5, high=lim[1] - 0.5, size=points_initial)
    f2 = interp1d(x, y, kind='cubic')
    trajectory_x = np.linspace(0, 10, num=points_generated, endpoint=True).reshape(-1, 1)
    trajectory_y = f2(trajectory_x)
    trajectory = np.concatenate((trajectory_x, trajectory_y), axis=1)
    return trajectory


def calc_normal(vector):
    normal = np.zeros(vector.shape)
    normal[0] = vector[1]
    normal[1] = - vector[0]
    return normal


class Disturber:
    def __init__(self, trajectory, radius=0.5):
        self.trajectory = trajectory
        self.radius = radius
        self.current_pos = trajectory[0, :]
        self.current_dir = np.zeros(2)
        self.normal = np.zeros(2)

    def move(self, i):
        self.current_dir = (self.trajectory[i, :] - self.current_pos).reshape(-1, 1)
        self.current_dir = normalize(self.current_dir, axis=0)
        self.current_pos = self.trajectory[i, :]
        self.normal = calc_normal(self.current_dir)
        return self.current_pos


class Drone:
    def __init__(self, radius=0.5, initial_pos=np.array([5, 5]), step=0.05, dist_permitted=2):
        self.radius = radius,
        self.initial_pos = initial_pos
        self.dist_permitted = dist_permitted
        self.current_pos = initial_pos
        self.step = step

    def move(self, normal):
        self.current_pos = self.current_pos + self.step * normal
        # return self.current_pos

    def move_back(self):
        self.current_pos = self.current_pos + self.step * (self.initial_pos - self.current_pos)
        # return self.current_pos


disturber = Disturber(create_random_trajectory())
drone = Drone()

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                     xlim=lim, ylim=lim)
ax.grid()

line_dis, = ax.plot([], [], '-', lw=2)
pos_dis, = ax.plot([], [], 'o', lw=3, c='b')
line_drone, = ax.plot([], [], 'x', markersize=8, lw=3, c='b')


# ------------------------------------------------------------
# set up figure and animation

def animate(i):
    global disturber, drone
    line_dis.set_data(disturber.trajectory[:i, :].T)
    pos_dis.set_data(disturber.current_pos)
    distance = np.linalg.norm(disturber.current_pos - drone.current_pos)

    if distance < drone.dist_permitted:
        line_drone.set_color('r')
        normal = disturber.normal.ravel()
        normal = normal * np.sign(np.dot(drone.current_pos - disturber.current_pos, normal))
        drone.move(normal)
    else:
        if (drone.initial_pos != drone.current_pos).any():
            drone.move_back()
        line_drone.set_color('b')
        line_drone.set_data(drone.current_pos)
    disturber.move(i)
    return line_dis, line_drone, pos_dis


def init():
    """initialize animation"""
    line_dis.set_data([], [])
    line_drone.set_data([], [])
    pos_dis.set_data([], [])
    return line_dis, line_drone, pos_dis


ani = animation.FuncAnimation(fig, animate, frames=n_frames,
                              interval=10, blit=True, init_func=init)

plt.show()
