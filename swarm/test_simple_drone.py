import numpy as np

from simple_drone import Disturber, Drone
from visualization import SceneVisualization
from utils import create_random_trajectory


if __name__ == '__main__':
    n_frames = 500
    lim = (0, 10)

    agents = list()
    agents.append(Disturber(agents, create_random_trajectory(7, n_frames, lim)))
    agents.extend([Drone(agents, np.array([2, 5]), borders=lim),
                   Drone(agents, np.array([4, 5]), borders=lim),
                   Drone(agents, np.array([7, 7]), borders=lim),
                   Drone(agents, np.array([6, 5]), borders=lim),
                   Drone(agents, np.array([8, 1]), borders=lim),
                   Drone(agents, np.array([8, 8]), borders=lim),
                   Drone(agents, np.array([1, 8]), borders=lim)])

    scene = SceneVisualization(agents, lim, 100, n_frames, 2)
    scene.mainloop()
