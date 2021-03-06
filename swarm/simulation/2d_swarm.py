import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
from scipy.interpolate import interp1d
from sklearn.preprocessing import normalize
import collections

low = 0
high = 10
n_frames = 1000
np.random.seed(21)


def create_trajectory(points_initial=7, points_generated=n_frames):
    x = np.linspace(low, high, num=points_initial)
    y = np.random.uniform(low=low + 0.5, high=high - 0.5, size=points_initial)
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

def flatten(some_list):
    for el in some_list:
        if isinstance(el, collections.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el

trajectory = create_trajectory()


class Disturber:
    """disturber"""

    def __init__(self, radius = 0.5):
                self.radius = radius
                self.current_pos = trajectory[0, :]
                self.current_dir = np.zeros(2)
                self.normal = np.zeros(2)

    def move(self, i):
        self.current_dir = (trajectory[i, :] - self.current_pos).reshape(-1, 1)
        self.current_dir = normalize(self.current_dir, axis=0)
        self.current_pos = trajectory[i, :]
        self.normal = calc_normal(self.current_dir)
        return self.current_pos


class Drone:
    """Drone"""
    def __init__(self,
                radius = 0.5,
                initial_pos = np.array([5, 5]),
                step = 0.05,
                dist_permitted = 2):

                self.radius = radius,
                self.initial_pos = initial_pos
                self.dist_permitted = dist_permitted
                self.current_pos = initial_pos
                self.step = step

    def move(self, normal):
        self.current_pos = self.current_pos + self.step * normal
        #return self.current_pos

    def move_back(self):
        self.current_pos = self.current_pos + self.step * (self.initial_pos - self.current_pos)
        #return self.current_pos

dis = Disturber()
drone = Drone()
swarm = [Drone(initial_pos=np.array([2, 2])), Drone(initial_pos=np.array([5, 2])), Drone(initial_pos=np.array([7, 7]))]
fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                     xlim=(low, high), ylim=(low, high))
ax.grid()

line_dis, = ax.plot([], [], '-', lw=2)
pos_dis, = ax.plot([], [], 'o', lw=3, c='b')
line_drone_list = [ax.plot([], [], 'x', markersize=8, lw=3, c='b')[0] for _ in swarm]
print(type(pos_dis))

#------------------------------------------------------------
# set up figure and animation

def animate(i):
    #global dis, drone
    line_dis.set_data(trajectory[:i, :].T)
    pos_dis.set_data(dis.current_pos)
    for num, drone in enumerate(swarm):
        distance = np.linalg.norm(dis.current_pos - drone.current_pos)
        if num==0:
            print(distance)
        if distance < drone.dist_permitted:
            line_drone_list[num].set_color('r')
            normal = dis.normal.ravel()
            normal = normal * np.sign(np.dot(drone.current_pos - dis.current_pos, normal))
            drone.move(normal)
        else:
            if (drone.initial_pos != drone.current_pos).any():
                drone.move_back()
            line_drone_list[num].set_color('b')
            line_drone_list[num].set_data(drone.current_pos)
    dis.move(i)
    output = tuple(flatten([line_dis, line_drone_list, pos_dis]))
    return output

def init():
    """initialize animation"""
    line_dis.set_data([], [])
    for elem in line_drone_list:
        elem.set_data([], [])
    pos_dis.set_data([], [])
    output = tuple(flatten([line_dis, line_drone_list, pos_dis]))
    return output

ani = animation.FuncAnimation(fig, animate, frames=n_frames,
                              interval=10, blit=True, init_func=init)

plt.show()