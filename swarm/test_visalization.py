from agent import TrajectoryAgent
from visualization import SceneVisualization
from utils import create_random_trajectory


if __name__ == '__main__':
    n_frames = 500
    lim = (0, 10)

    agents = []
    agents.extend([TrajectoryAgent(agents, create_random_trajectory(7, n_frames, lim)),
                   TrajectoryAgent(agents, create_random_trajectory(7, n_frames, lim))])

    scene = SceneVisualization(agents, lim, 100, n_frames, 2)
    scene.mainloop()
