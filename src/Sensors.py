import numpy as np
import scipy.io as sio
from Environment import Environment

class DefaultSensor:
    label = "Default Sensor"

    def __init__(self, environment, handle):
        self.env = environment
        self.robot_handle = handle
        
    def sense(self):
        raise NotImplementedError()
