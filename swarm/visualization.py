import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
from scipy.interpolate import interp1d
from sklearn.preprocessing import normalize


class SceneVisualization:
    def __init__(self, agents, lim):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, aspect='equal', autoscale_on=False, xlim=lim, ylim=lim)
        self.ax.grid()

        self.agents = agents

        self.line_dis, = self.ax.plot([], [], '-', lw=2)
        self.pos_dis, = self.ax.plot([], [], 'o', lw=3, c='b')
        self.line_drone, = self.ax.plot([], [], 'x', markersize=8, lw=3, c='b')

    def clear_plot(self):
        self.line_dis.set_data([], [])
        self.line_drone.set_data([], [])
        self.pos_dis.set_data([], [])
        return self.line_dis, self.line_drone, self.pos_dis

    def do_model_step(self, i):
        line_dis, = self.ax.plot([], [], '-', lw=2)
        pos_dis, = self.ax.plot([], [], 'o', lw=3, c='b')
        line_drone, = self.ax.plot([], [], 'x', markersize=8, lw=3, c='b')

        #line_dis.set_data(disturber.trajectory[:i, :].T)
        #pos_dis.set_data(disturber.current_pos)

        #line_drone.set_color('r')

        #line_drone.set_color('b')
        #line_drone.set_data(drone.current_pos)




ani = animation.FuncAnimation(fig, animate, frames=n_frames,
                              interval=10, blit=True, init_func=init)

plt.show()
