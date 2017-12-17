import numpy as np

from simple_drone import Drone, Disturber


def get_drone_real_position(drone_id):
    return room.ask_about_drone_position(drone_id)


def send_drone_real_desired_position(drone_id, position):
    room.send_drone_real_desired_position(drone_id, position)


def get_disturber_real_position():
    return room.ask_about_disturber_position


lim = (0, 10)

agents = list()
agents.append(Disturber(agents, ))
agents.extend([Drone(agents, np.array([2, 5]), borders=lim),
               Drone(agents, np.array([4, 5]), borders=lim),
               Drone(agents, np.array([7, 7]), borders=lim)])

while True:
    agents[0].update_position(get_disturber_real_position())

    # First get real positions
    for i, agent in enumerate(agents[1:]):
        agent.update_position(get_drone_real_position(i))
        
    # Then make decisions
    for i, agent in enumerate(agents[1:]):
        send_drone_real_desired_position(i, agent.get_next_position())
