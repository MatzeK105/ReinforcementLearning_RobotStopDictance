import numpy as np
import pandas as pd

class RL(object):

    def __init__(self, action_space, learning_rate=0.01, gamma=0.99, epsilon=0.99):
        self.actions = action_space
        self.lr = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)

    def add_state_if_not_exists(self, state):
        if state not in self.q_table.index:
            # append new state to q table
            self.q_table = self.q_table.append(
                pd.Series(
                    [0]*len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                )
            )

    def choose_action(self, state):
        self.add_state_if_not_exists(state)
        # action selection
        if np.random.rand() < self.epsilon:
            # choose best action
            state_action = self.q_table.ix[state, :]
            # if all actions have same value, idxmax picks the first action, that's why shuffle the list
            state_action = state_action.reindex(np.random.permutation(state_action.index))
            action = state_action.idxmax()
        else:
            # choose random action
            action = np.random.choice(self.actions)

        return action

class Sarsa(RL):

    def __init__(self, actions, learning_rate=0.01, gamma=0.99, epsilon=0.99):
        super(Sarsa, self).__init__(actions, learning_rate, gamma, epsilon)

    def learn(self, s, a, r, s_, a_, finished):
        self.add_state_if_not_exists(s_)
        q_predict = self.q_table.ix[s, a]

        if not finished:
            q_target = r + self.gamma * self.q_table.ix[s_, a_]
        else:
            q_target = r

        self.q_table.ix[s, a] += self.lr * (q_target - q_predict)  # update