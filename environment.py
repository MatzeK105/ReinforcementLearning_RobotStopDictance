import numpy as np
import tkinter as tk
import time

HEIGHT = 100
WIDTH = 800
ROBOT_START_X = 200
ROBOT_START_Y = 50
SLEEP_TIME = 0.0005
SLEEP_TIME_RESET = 0.5

class Environment(tk.Tk, object):
    def __init__(self):
        super(Environment, self).__init__()
        self.action_space = ['g', 'b']  # go, break
        self.num_actions = len(self.action_space)
        self.title('Environment')
        self.geometry('{0}x{1}'.format(WIDTH, HEIGHT))
        self._build_environment()

    def _build_environment(self):
        self.canvas = tk.Canvas(self, bg='white', height=HEIGHT, width=WIDTH)

        # create obstacle
        obstacle_center = np.array([20, 50])
        self.obstacle = self.canvas.create_rectangle(
            obstacle_center[0] - 10, obstacle_center[1] - 40,
            obstacle_center[0] + 10, obstacle_center[1] + 40,
            fill='black'
        )

        # create robot
        robot_center = np.array([ROBOT_START_X, ROBOT_START_Y])
        self.robot = self.canvas.create_polygon([
            robot_center[0] - 25, robot_center[1] + 10, robot_center[0] - 25, robot_center[1] - 10,
            robot_center[0] - 15, robot_center[1] - 10, robot_center[0] - 15, robot_center[1] - 25,
            robot_center[0] + 25, robot_center[1] - 25, robot_center[0] + 25, robot_center[1] + 25,
            robot_center[0] - 15, robot_center[1] + 25, robot_center[0] - 15, robot_center[1] + 10
            ], 
            fill='blue'
        )

        # pack
        self.canvas.pack()

    def perform_action(self, action):
        stopped = False
        done = False
        reward = 0

        if action == 0:     # drive
            self.canvas.move(self.robot, -1, 0)
        elif action == 1:   # break
            self.canvas.move(self.robot, -50, 0)    # move further because of stop distance
            stopped = True

        nextState = self.canvas.coords(self.robot)
        obstCoords = self.canvas.coords(self.obstacle)
        dist = nextState[0] - obstCoords[2]

        if stopped:
            if (dist >= 15 and dist <= 40):     # if enough space to obstacle
                reward = 1
                done = True
            elif dist < 15:
                reward = -1
                done = True
            else:
                reward = -1
                done = False
        elif nextState[0] <= obstCoords[2]:   # if robot hits obstacle
            reward = -1
            done = True

        return dist, reward, done

    def reset(self):
        self.update()
        time.sleep(SLEEP_TIME_RESET)
        self.canvas.delete(self.robot)

        # create robot
        robot_center = np.array([ROBOT_START_X, ROBOT_START_Y])
        self.robot = self.canvas.create_polygon([
            robot_center[0] - 25, robot_center[1] + 10, robot_center[0] - 25, robot_center[1] - 10,
            robot_center[0] - 15, robot_center[1] - 10, robot_center[0] - 15, robot_center[1] - 25,
            robot_center[0] + 25, robot_center[1] - 25, robot_center[0] + 25, robot_center[1] + 25,
            robot_center[0] - 15, robot_center[1] + 25, robot_center[0] - 15, robot_center[1] + 10
            ], 
            fill='blue'
        )

        robotCoords = self.canvas.coords(self.robot)
        obstCoords = self.canvas.coords(self.obstacle)
        dist = robotCoords[0] - obstCoords[2]

        return dist

    def render(self):
        time.sleep(SLEEP_TIME)
        self.update()