import numpy as np
from copy import deepcopy
from Nim import Nim
import matplotlib.pyplot as plt
import random

class Agent(object):
    def __init__(self, alpha=0.15, random_factor=0.2):  # 80% explore, 20% exploit
        self.state_history = []  # state, reward
        self.alpha = alpha
        self.random_factor = random_factor
        self.G = {}
        # This two are used just to save and have a graphical plot of the "loss" while learning
        self.moveHistory = []
        self.indices = []
        self.steps = 1 

    def init_reward(self):
        return np.random.uniform(low=1.0, high=0.1)

    def choose_action(self, state: Nim, allowedMoves):
        maxG = -10e15
        next_move = None
        randomN = np.random.random()
        if randomN < self.random_factor:
            # if random number below random factor, choose random action
            next_move = random.choice(allowedMoves)
            state.nimming(next_move)
            if state not in self.G.keys():
                self.G[state.__str__()] = self.init_reward()

        else:
            # if exploiting, gather all possible actions and choose one with the highest G (reward)
            for action in allowedMoves:
                new_state = deepcopy(state)
                new_state.nimming(action)

                if new_state not in self.G.keys():
                    self.G[new_state.__str__()] = self.init_reward()

                if self.G[new_state.__str__()] >= maxG:
                    next_move = action
                    maxG = self.G[new_state.__str__()]

        return next_move

    def update_state_history(self, state, reward):
        self.state_history.append((state, reward))

    def learn(self):
        target = 0

        for prev, reward in reversed(self.state_history):
            self.G[prev.__str__()] = self.G[prev.__str__()] + self.alpha * (target - self.G[prev.__str__()])
            target += reward

        self.state_history = []

        self.random_factor -= 10e-5  # decrease random factor each episode of play


    def play(self, opponent, state: Nim):
        nim = state
        # As in minmax, True is "us" while False is the opponent
        player = True

        for i in range(5000):
            self.steps += 1

            while not state.is_over():
                # state, _ = state.get_state_and_reward()  # get the current state
                state_copy = deepcopy(state)
                # choose an action (explore or exploit)
                action = self.choose_action(state_copy, state_copy.possible_moves())
                state.nimming(action)  # update the maze according to the action
                state, reward = state.get_state_and_reward()  # get the new state and reward
                # update the robot memory with state and reward
                self.update_state_history(state, reward)

            self.learn()  # robot should learn after every episode
            # get a history of number of steps taken to plot later
            if i % 50 == 0:
                print(f"{i}: {self.steps}")
                self.moveHistory.append(self.steps)
                self.indices.append(i)
            
            state = nim  # reinitialize the nim

        plt.semilogy(self.indices, self.moveHistory, "b")
        plt.show()
