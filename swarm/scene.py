import numpy as np
from sklearn.preprocessing import normalize
from utils import calc_normal


class Disturber:
    """Disturber"""
    def __init__(self,
                radius=1,
                initial_pos=np.array([5, 5]),
                step=0.1):

                self.radius = radius
                self.initial_pos = initial_pos
                self.current_pos = initial_pos
                self.previous_pos = initial_pos
                self.step = step
                self.direction = np.zeros(2)
                self.normal = np.zeros(2)

    def set_position(self, position):
        self.previous_pos = self.current_pos
        self.current_pos = position
        self.direction = normalize((self.current_pos - self.previous_pos).reshape(1, -1)).ravel()
        self.normal = calc_normal(self.direction)


class Drone:
    """Drone"""
    def __init__(self,
                radius=1,
                initial_pos=np.array([5, 5]),
                step=0.1):

                self.radius = radius
                self.initial_pos = initial_pos
                self.current_pos = initial_pos
                self.previous_pos = initial_pos
                self.next_pos = initial_pos
                self.step = step
                self.direction = np.zeros(2)
                self.normal = np.zeros(2)

    def set_position(self, position):
        self.current_pos = position

    def move(self):
        self.previous_pos = self.current_pos
        self.current_pos = self.next_pos
        self.direction = self.current_pos - self.previous_pos
        self.normal = calc_normal(self.direction)


class Scene:
    """Scene"""
    def __init__(self,
                 disturber=Disturber(),
                 drones=(Drone(), Drone(), Drone())):

        self.drones = drones
        self.swarm_position = [drone.current_pos for drone in self.drones]
        self.time = 0
        self.disturber = disturber

    def set_position(self, swarm_position, disturber_position):
        self.swarm_position = swarm_position
        self.disturber.set_position(disturber_position)
        for i, drone in enumerate(self.drones):
            drone.current_pos = swarm_position[i]

    def get_next_position(self):
        for drone in self.drones:
            if (np.linalg.norm(drone.current_pos - self.disturber.current_pos)) <= (drone.radius + self.disturber.radius):
                normal = self.disturber.normal.ravel() * np.sign(np.dot(drone.current_pos - self.disturber.current_pos, self.disturber.normal.ravel()))
                next_pos = drone.current_pos + drone.step * normal
                drone.next_pos = next_pos
            else:
                drone.next_pos = drone.current_pos
        return [drone.next_pos for drone in self.drones]

    def update_scene(self, swarm_position, disturber_position):
        self.set_position(swarm_position, disturber_position)
        self.get_next_position()
        [drone.move() for drone in self.drones]
