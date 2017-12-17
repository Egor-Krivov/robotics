import numpy as np
from sklearn.preprocessing import normalize
from utils import calc_normal

from agent import Agent

norm = np.linalg.norm


class Disturber(Agent):
    def __init__(self, agents, initial_position, radius=1, step=0.1):
        super().__init__(agents, initial_position)
        self.radius = radius
        self.step = step
        self.velocity_dir = np.zeros(2)
        self.normal = np.zeros(2)

    def update_position(self, position):
        self.velocity_dir = normalize((position - self.position).reshape(1, -1)).ravel()
        super().update_position(position)

        self.normal = calc_normal(self.velocity_dir)


class TrajectoryDisturber(Disturber):
    def __init__(self, agents, trajectory, radius=1, step=0.1):
        self.iteration = 0
        self.trajectory = trajectory

        super().__init__(agents, trajectory[self.iteration], radius, step)

    def get_next_position(self):
        self.iteration += 1
        return self.trajectory[self.iteration]


class Drone(Agent):
    def __init__(self, agents: [Agent], initial_position, borders, radius=1, step=0.1):
        super().__init__(agents, initial_position=initial_position)

        self.borders = borders
        self.radius = radius
        self.step = step
        self.velocity_dir = np.zeros(2)
        self.normal = np.zeros(2)

    def update_position(self, position):
        self.velocity_dir = normalize((position - self.position).reshape(1, -1)).ravel()
        super().update_position(position)

        self.normal = calc_normal(self.velocity_dir)

    def get_next_position(self):
        force = np.zeros_like(self.position, dtype=float)
        for agent in self.agents:
            if agent is self:
                continue
            elif isinstance(agent, Disturber) or isinstance(agent, Drone):
                if norm(self.position - agent.position) <= (self.radius + agent.radius):
                    force += agent.normal.ravel() * np.sign(np.dot(self.position - agent.position, agent.normal.ravel()))

        force += compute_border_force(self.position, self.radius, self.borders)

        return self.position + self.step * force


def compute_border_force(position, radius, borders):
    # interaction with borders
    force = np.zeros_like(position)
    if np.abs(position[0] - borders[0]) < radius:
        force += np.array([1, 0])
    if np.abs(position[0] - borders[1]) < radius:
        force += np.array([-1, 0])
    if np.abs(position[1] - borders[0]) < radius:
        force += np.array([0, 1])
    if np.abs(position[1] - borders[1]) < radius:
        force += np.array([0, -1])
    return force
