class Agent:
    def __init__(self, agents, initial_position):
        self.agents = agents
        self.position = initial_position

    def update_position(self, position):
        self.position = position

    def get_next_position(self):
        return self.position


class TrajectoryAgent(Agent):
    def __init__(self, agents, trajectory):
        self.iteration = 0
        self.trajectory = trajectory

        super().__init__(agents, trajectory[self.iteration])

    def get_next_position(self):
        self.iteration += 1
        return self.trajectory[self.iteration]
