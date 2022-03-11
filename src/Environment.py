import numpy as np
import scipy.io as sio
from isaacgym import gymapi, gymutil
from scipy.spatial.transform import Rotation as R

class Environment:
    # Different sensor types for robots in the swarm. Each sensor is a "device" located in "each robot". This class put
    # all sensor outputs of all robots in a single matrix for convenience.
    def __init__(self, sim, size, groundFile = None):        
        gym = gymapi.acquire_gym()
        self.sim = sim
        self.size = size
        
        # %% Initialize environment
        # print("Initialize environment")
        # Add ground plane
        plane_params = gymapi.PlaneParams()
        plane_params.normal = gymapi.Vec3(0, 0, 1)  # z-up!
        plane_params.distance = 0
        plane_params.static_friction = 0
        plane_params.dynamic_friction = 0
        gym.add_ground(self.sim, plane_params)

        # Set up the env grid
        num_envs = 1
        env_lower = gymapi.Vec3(-size[0]/2, -size[1]/2, 0.0)
        env_upper = gymapi.Vec3(size[0]/2, size[1]/2, size[0])

        self.gym_env = gym.create_env(self.sim, env_lower, env_upper, num_envs)

    def add_robot(self,robotClass,controller,name):
        gym = gymapi.acquire_gym()
        
        pose = gymapi.Transform()
        pose.p = gymapi.Vec3(np.random.uniform(-self.size[0]/2,self.size[0]/2), np.random.uniform(-self.size[1]/2,self.size[1]/2), 0.1)
        rot = R.from_euler('z', np.random.randint(0,360), degrees=True).as_quat()
        pose.r = gymapi.Quat(rot[0],rot[1],rot[2],rot[3])

        robot_asset = gym.load_asset(self.sim, robotClass.asset_root, robotClass.robot_asset_file, robotClass.asset_options)
        if robot_asset is None:
            print("*** Failed to load robot asset at",asset_root,robot_asset_file)
            quit()

        robot = robotClass(name,controller,self,gym.create_actor(self.gym_env, robot_asset, pose, name, 0, 0))

        # get joint limits and ranges for robot
        props = gym.get_actor_dof_properties(self.gym_env, robot.handle)
            
        # Give a desired velocity to drive
        props["driveMode"].fill(gymapi.DOF_MODE_VEL)
        props["stiffness"].fill(0)
        props["damping"].fill(10)
        velocity_limits = props["velocity"]
        gym.set_actor_dof_properties(self.gym_env, robot.handle, props)

        return robot

    
