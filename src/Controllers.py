import numpy as np
from Actuators import Diff_Wheels

class Controller(object):
    def __init__(self, robot):
        self.controller_type = "default"
        self.umax_const = 0.1
        self.wmax = 1.5708 / 2.5

    def step(self):
        raise NotImplementedError()

class RandomWalk(Controller):
    def __init__(self, robot):
        self.controller_type = "random_walk"
        self.max_steps = 180
        self.turning = True
        self.wheels = robot.addActuator(Diff_Wheels)
        self.action()

    def action(self):
        self.turning = not self.turning
        if(self.turning):
            self.decision_steps = np.random.randint(0,self.max_steps)
            if(np.random.randint(0,2)):
                self.current_velocity = (-6, 6)
            else:
                self.current_velocity = (6, -6)
        else:
            self.decision_steps = self.max_steps
            self.current_velocity = (6,6)
    
    def step(self):
        if(self.decision_steps <= 0):
            self.action()
        self.decision_steps-=1
        self.wheels.drive(self.current_velocity[0],self.current_velocity[1])
