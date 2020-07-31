import random
from collections import deque

import numpy as np


class ReplayMemory:
    def __init__(self, buffer_size):
        self.buffer = deque()
        self.buffer_size = buffer_size

    def add(self, episode_experience):
        self.buffer.append(episode_experience)
        if len(self.buffer) > self.buffer_size:
            self.buffer.popleft()

    def sample(self, batch_size, trace_length):
        sampled_episodes = random.sample(self.buffer, batch_size)
        sampledTraces = []
        for episode in sampled_episodes:
            point = np.random.randint(0, len(episode) + 1 - trace_length)
            sampledTraces.append(episode[point : point + trace_length])
        sampledTraces = np.array(sampledTraces)
        return sampledTraces
