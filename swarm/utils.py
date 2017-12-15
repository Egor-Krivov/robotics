import numpy as np
from scipy.interpolate import interp1d
import collections


def create_trajectory(low, high, points_initial=7, points_generated=1000):
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