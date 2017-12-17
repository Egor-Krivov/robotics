class Agent:
    def __init__(self, agents, initial_position):
        self.agents = agents
        self.position = initial_position

    def update_position(self, position):
        self.position = position

    def get_next_position(self):
        return self.position
