import numpy as np
import scipy.io as sio
from isaacgym import gymapi
from Environment import Environment

class Diff_Wheels:
    label = "Differential drive wheels"

    def __init__(self, environment, handle):
        self.env = environment
        self.robot_handle = handle
        
    def drive(self,left_speed,right_speed):
        gym = gymapi.acquire_gym()
        gym.set_actor_dof_velocity_targets(self.env.gym_env, self.robot_handle, (left_speed,right_speed))
