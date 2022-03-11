from isaacgym import gymapi, gymutil

class Thymio(object):
    asset_options = gymapi.AssetOptions()
    asset_options.fix_base_link = False
    asset_options.armature = 0.0001

    asset_root = "../models"
    robot_asset_file = "thymio/model.urdf"
    
    def __init__(self, name, controllerClass, env, handle):
        self.name = name        
        self.env = env
        self.handle = handle

        self.sensors = []
        self.actuators = []

        self.controller = controllerClass(self)

    def addSensor(self,sensorClass):
        self.sensors.append(sensorClass(self.env,self.handle))
        return self.sensors[-1]

    def addActuator(self,actuatorClass):
        self.actuators.append(actuatorClass(self.env,self.handle))
        return self.actuators[-1]

    def step(self):
        self.controller.step()
