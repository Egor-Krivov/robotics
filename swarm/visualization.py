from collections import deque

import matplotlib.pyplot as plt
import matplotlib.animation as animation

from agent import Agent


def make_agent_tracker(agent: Agent, track_len):
    track = deque([agent.position], maxlen=track_len)

    def get_next_track():
        track.append(agent.get_next_position())
        agent.update_position(track[-1])
        return track

    return get_next_track


class SceneVisualization:
    def __init__(self, agents: [Agent], lim, track_len, n_frames, ndim):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, aspect='equal', autoscale_on=False, xlim=lim, ylim=lim)
        self.ax.grid()

        self.ndim = ndim
        self.n_frames = n_frames
        self.agent_trackers = [make_agent_tracker(agent, track_len) for agent in agents]

    def init_plot(self):
        self.agents_lines = self.ax.plot(*[[] for _ in range(2 * len(self.agent_trackers))], '-', lw=2)
        self.agents_positions = [self.ax.plot([], [], 'o', lw=3)[0] for _ in range(len(self.agent_trackers))]

        return (*self.agents_lines, *self.agents_positions)

    def do_model_step(self, i):
        for i, track_agent in enumerate(self.agent_trackers):
            track = track_agent()
            self.agents_lines[i].set_data(*[[point[i] for point in track] for i in range(self.ndim)])
            self.agents_positions[i].set_data(track[-1])

        return (*self.agents_lines, *self.agents_positions)

    def mainloop(self):
        ani = animation.FuncAnimation(self.fig, self.do_model_step, interval=20, blit=True, init_func=self.init_plot)
        plt.show()
