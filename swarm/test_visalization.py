import numpy as np
from scipy.interpolate import interp1d

from agent import TrajectoryAgent
from visualization import SceneVisualization


def create_random_trajectory(points_initial, points_generated):
    x = np.linspace(*lim, num=points_initial)
    y = np.random.uniform(low=lim[0] + 0.5, high=lim[1] - 0.5, size=points_initial)
    f2 = interp1d(x, y, kind='cubic')
    trajectory_x = np.linspace(0, 10, num=points_generated, endpoint=True).reshape(-1, 1)
    trajectory_y = f2(trajectory_x)
    trajectory = np.concatenate((trajectory_x, trajectory_y), axis=1)
    return trajectory


if __name__ == '__main__':
    n_frames = 500
    lim = (0, 10)

    agents = []
    agent = TrajectoryAgent(create_random_trajectory(7, n_frames), agents)

    agents.append(agent)
    scene = SceneVisualization(agents, lim, 100, n_frames, 2)
    scene.mainloop()
    import time
    time.sleep(1000)
