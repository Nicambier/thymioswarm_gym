import sys
import os
import math
import time
from multiprocessing import Process, Queue
import numpy as np
from isaacgym import gymapi, gymutil
from scipy.spatial.transform import Rotation as R
from Thymio import Thymio
from Environment import Environment
from Controllers import RandomWalk

def launch_sim(NB_ROBOTS, exp_time, headless = False):
    # %% Initialize gym
    gym = gymapi.acquire_gym()

    # Parse arguments
    args = gymutil.parse_arguments(description="Loading and testing")

    # configure sim
    sim_params = gymapi.SimParams()
    sim_params.dt = 0.1
    sim_params.substeps = 2

    # defining axis of rotation!
    sim_params.up_axis = gymapi.UP_AXIS_Z
    sim_params.gravity = gymapi.Vec3(0.0, 0.0, -9.81)

    sim_params.physx.solver_type = 1
    sim_params.physx.num_position_iterations = 4
    sim_params.physx.num_velocity_iterations = 1
    sim_params.physx.num_threads = args.num_threads
    sim_params.physx.use_gpu = True

    sim = gym.create_sim(args.compute_device_id, args.graphics_device_id, args.physics_engine, sim_params)
    if sim is None:
        print("*** Failed to create sim")
        quit()

    # create viewer
    viewer = None
    if not headless:
        viewer = gym.create_viewer(sim, gymapi.CameraProperties())
        if viewer is None:
            print("*** Failed to create viewer")
            quit()

    spacing = 3
    env = Environment(sim,(spacing,spacing),'Gradient Maps/circle_30x30.mat')

    # Point camera at environments
    iangle = 6.28 * np.random.rand()
    iy = spacing + 12 * (np.cos(iangle))
    ix = spacing + 12 * (np.sin(iangle))
    cam_pos = gymapi.Vec3(-2+ix, iy, 2)
    cam_target = gymapi.Vec3(0, 0, 0.0)
    gym.viewer_camera_look_at(viewer, None, cam_pos, cam_target)

    # # subscribe to spacebar event for reset
    gym.subscribe_viewer_keyboard_event(viewer, gymapi.KEY_R, "reset")

    thymios = []
    for i in range(NB_ROBOTS):
        pose = gymapi.Transform()
        pose.p = gymapi.Vec3(np.random.uniform(-spacing,spacing), np.random.uniform(-spacing,spacing), 0.1)
        rot = R.from_euler('z', np.random.randint(0,360), degrees=True).as_quat()
        pose.r = gymapi.Quat(rot[0],rot[1],rot[2],rot[3])
        thymios.append(env.add_robot(Thymio,RandomWalk,"robot_"+str(i)))

    t=0
    while t<exp_time and not gym.query_viewer_has_closed(viewer):
        for thymio in thymios:        
            thymio.step()
        
        # step the physics
        gym.simulate(sim)
        gym.fetch_results(sim, True)

        # update the viewer
        gym.step_graphics(sim)
        gym.draw_viewer(viewer, sim, True)

        # Wait for dt to elapse in real time.
        # This synchronizes the physics simulation with the rendering rate.
        gym.sync_frame_time(sim)
        t = gym.get_sim_time(sim)

    gym.destroy_viewer(viewer)
    gym.destroy_sim(sim)
    

def main(argv):
    p = Process(target=launch_sim, args=(15, 600, False))
    p.start()
    p.join() # this blocks until the process terminates

if __name__ == "__main__":
    main(sys.argv)
