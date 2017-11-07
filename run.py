from environment import Environment
import time

def update():
    done = False
    action = 0
    counter = 0
    time.sleep(2)

    while True:
        newState, reward, done = env.performAction(action)
        env.render()

        if done:
            counter += 1
            env.reset()
            if counter == 3:
                break

    time.sleep(2)
    print('end')
    env.destroy()

if __name__ == "__main__":
    env = Environment()

    env.after(100, update)
    env.mainloop()