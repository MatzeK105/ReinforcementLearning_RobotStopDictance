import numpy as np
import tkinter as tk
import time

HEIGHT = 100
WIDTH = 800
ROBOT_START_X = 700
ROBOT_START_Y = 50
SLEEP_TIME = 0.00001
SLEEP_TIME_RESET = 0.2

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

    def stop_robot(self):
        # change outline to show the robot slows down
        self.canvas.itemconfig(self.robot, outline='red')
        
        # slow down robot
        for i in range(50):
            self.canvas.move(self.robot, -1, 0)
            time.sleep(SLEEP_TIME * 10 * i)
            self.render()

        # change outline back again
        self.canvas.itemconfig(self.robot, outline='')
        self.render()
        time.sleep(0.2)

    def perform_action(self, action):
        stopped = False
        done = False
        reward = 0

        if action == 0:     # drive
            self.canvas.move(self.robot, -1, 0)
        elif action == 1:   # break
            # if you want to speed up the process comment the next line in and the function stop_robot out
            #self.canvas.move(self.robot, -50, 0)    # move further because of stop distance
            self.stop_robot()
            stopped = True

        nextState = self.canvas.coords(self.robot)
        obstCoords = self.canvas.coords(self.obstacle)
        dist = nextState[0] - obstCoords[2]

        if stopped:
            if (dist >= 15 and dist <= 40):     # if enough space to obstacle
                reward = 1
                done = True
            elif dist < 15:     # if too close to obstacle
                reward = -1
                done = True
            else:               # if too far away to obstacle
                reward = -1
                done = False
        elif nextState[0] <= obstCoords[2]:     # if robot hits obstacle
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