from environment import Environment
from rl_brain import Sarsa
import time

def update():
    for episode in range(300):
        done = False

        # init
        observation = env.reset()
        env.render()

        # rl choose action
        action = rl.choose_action(str(observation))

        while not done:
            observation_, reward, done = env.perform_action(action)
            env.render()

            # choose action for next observation
            action_ = rl.choose_action(str(observation_))

            rl.learn(str(observation), action, reward, str(observation_), action_, done)

            observation = observation_
            action = action_

    time.sleep(2)
    print('end')
    env.destroy()

if __name__ == "__main__":
    env = Environment()
    rl = Sarsa(actions=list(range(env.num_actions)))

    time.sleep(1)
    env.after(100, update)
    env.mainloop()