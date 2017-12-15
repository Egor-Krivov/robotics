class Agent:
    def __init__(self, agents, init_position):
        self.agents = agents
        self.position = init_position

    def set_position(self, position):
        self.position = position

    def get_next_position(self):
        return self.position


class TrajectoryAgent(Agent):
    def __init__(self, trajectory, agents):
        self.iteration = 0
        self.trajectory = trajectory

        super().__init__(agents, trajectory[self.iteration])

    def get_next_position(self):
        self.iteration += 1
        return self.trajectory[self.iteration]
