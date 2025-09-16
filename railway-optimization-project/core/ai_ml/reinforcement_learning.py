# core/ai_ml/reinforcement_learning.py
"""
Reinforcement learning for adaptive scheduling.
"""

import numpy as np
import random
from collections import defaultdict
import logging


class SchedulingAgent:
    """Q-learning agent for train scheduling."""

    def __init__(self, learning_rate=0.1, discount_factor=0.9, epsilon=0.1):
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.q_table = defaultdict(lambda: defaultdict(float))
        self.logger = logging.getLogger(__name__)

    def get_action(self, state, available_actions):
        """Choose action using epsilon-greedy policy."""
        if random.random() < self.epsilon:
            # Exploration
            return random.choice(available_actions)
        else:
            # Exploitation
            q_values = {action: self.q_table[state][action]
                        for action in available_actions}
            return max(q_values, key=q_values.get)

    def update_q_value(self, state, action, reward, next_state, next_actions):
        """Update Q-value using Q-learning rule."""
        if next_actions:
            max_next_q = max(self.q_table[next_state][a] for a in next_actions)
        else:
            max_next_q = 0

        current_q = self.q_table[state][action]
        new_q = current_q + self.lr * (reward + self.gamma * max_next_q - current_q)

        self.q_table[state][action] = new_q

    def train_episode(self, environment):
        """Train agent for one episode."""
        state = environment.reset()
        total_reward = 0

        while not environment.is_done():
            available_actions = environment.get_available_actions()
            action = self.get_action(state, available_actions)

            next_state, reward, done = environment.step(action)
            next_actions = environment.get_available_actions() if not done else []

            self.update_q_value(state, action, reward, next_state, next_actions)

            state = next_state
            total_reward += reward

        return total_reward


