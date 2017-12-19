import numpy as np
from sklearn.preprocessing import normalize
from utils import calc_normal, calc_dir
from  itertools import permutations, combinations


class Disturber:
    """Disturber"""
    def __init__(self,
                radius=0.2,
                initial_pos=np.array([5, 5]),
                step=0.1):

                self.radius = radius
                self.initial_pos = initial_pos
                self.current_pos = initial_pos
                self.previous_pos = initial_pos
                self.step = step
                self.velocity_dir = np.zeros(2)
                self.force_dir = self.velocity_dir
                self.normal = np.zeros(2)
                self.memory = [self.initial_pos] * 10

    def set_position(self, position): 
        self.memory.append(position)
        self.memory.pop(0)
        self.previous_pos = self.current_pos
        self.current_pos = position
        #self.velocity_dir = normalize((self.current_pos - self.previous_pos).reshape(1, -1)).ravel()
        self.velocity_dir = normalize(calc_dir(np.array(self.memory)).reshape(1, -1)).ravel()
        self.force_dir = self.velocity_dir
        self.normal = calc_normal(self.velocity_dir)


class Drone:
    """Drone"""
    def __init__(self,
                radius=0.2,
                initial_pos=np.array([5, 5]),
                step=0.05,
                drone_id=0):

                self.radius = radius
                self.initial_pos = initial_pos
                self.current_pos = initial_pos
                self.previous_pos = initial_pos
                self.next_pos = initial_pos
                self.step = step
                self.velocity_dir = np.zeros(2)
                self.normal = np.zeros(2)
                self.force_dir = np.zeros(2)
                self.drone_id = drone_id
    def set_position(self, position):
        self.current_pos = position

    def move(self):
        self.previous_pos = self.current_pos
        self.current_pos = self.next_pos
        self.velocity_dir = self.current_pos - self.previous_pos
        self.normal = calc_normal(self.velocity_dir)


class Scene:
    """Scene"""
    def __init__(self,
                 disturber=Disturber(),
                 drones=(Drone(), Drone(), Drone()),
                 eps = 0.05):

        self.drones = drones
        self.swarm_position = [drone.current_pos for drone in self.drones]
        self.time = 0
        self.disturber = disturber
        self.borders = (-1, 1)
        self.eps = eps

    def set_position(self, swarm_position, disturber_position):
        self.swarm_position = swarm_position
        self.disturber.set_position(disturber_position)
        for i, drone in enumerate(self.drones):
            drone.current_pos = swarm_position[i]

    def get_next_position(self):

        for drone in self.drones:
            drone.next_pos = drone.current_pos + drone.step * drone.force_dir

        return [drone.next_pos for drone in self.drones]

    def calculate_forces(self):

        # interaction with disturber
        for drone in self.drones:
            if (np.linalg.norm(drone.current_pos - self.disturber.current_pos)) <= (drone.radius + self.disturber.radius):
                force_dir = self.disturber.normal.ravel() * np.sign(np.dot(drone.current_pos - self.disturber.current_pos, self.disturber.normal.ravel()))
                #force_dir = normalize((drone.current_pos - self.disturber.current_pos).reshape(1, -1)).ravel()
                drone.force_dir = force_dir
                print('ALARM!!')
            else:
                drone.force_dir=np.zeros(2)

        # interaction eith other drones
        """for drone_pair in combinations(self.drones, r=2):
            if np.linalg.norm(drone_pair[0].current_pos - drone_pair[1].current_pos) <= (drone_pair[0].radius + drone_pair[1].radius):
                force_dir = normalize((drone_pair[0].current_pos - drone_pair[1].current_pos).reshape(1, -1)).ravel()
                drone_pair[0].force_dir += force_dir
                drone_pair[1].force_dir -= force_dir

        # interaction with borders
        for drone in self.drones:
            if np.abs(drone.current_pos[0] - self.borders[0]) < drone.radius:
                force_dir = np.array([1, 0])
                drone.force_dir += force_dir
            if np.abs(drone.current_pos[0] - self.borders[1]) < drone.radius:
                force_dir = np.array([-1, 0])
                drone.force_dir += force_dir
            if np.abs(drone.current_pos[1] - self.borders[0]) < drone.radius:
                force_dir = np.array([0, 1])
                drone.force_dir += force_dir
            if np.abs(drone.current_pos[1] - self.borders[1]) < drone.radius:
                force_dir = np.array([0, -1])
                drone.force_dir += force_dir

        # moving back to initial point if there is no danger
        for drone in self.drones:
            if np.linalg.norm(drone.force_dir) == 0:
                if np.linalg.norm(drone.current_pos - drone.initial_pos) >= self.eps:
                    force_dir = normalize((drone.initial_pos - drone.current_pos).reshape(1, -1)).ravel()
                    drone.force_dir = force_dir
            drone.force_dir = normalize(drone.force_dir.reshape(1, -1)).ravel()"""

    def update_scene(self, swarm_position, disturber_position):
        self.set_position(swarm_position, disturber_position)
        self.calculate_forces()
        self.get_next_position()
        [drone.move() for drone in self.drones]
