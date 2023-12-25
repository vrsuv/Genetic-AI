import pybullet as p
import pybullet_data as pd

p.connect(p.GUI)
p.setPhysicsEngineParameter(enableFileCaching=0)
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
plane_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(plane_shape, plane_shape)
p.setGravity(0, 0, -10)

# import time
# while True:
#     p.stepSimulation()
#     time.sleep(1.0/240)


# import pybullet
# pybullet.connect(pybullet.GUI)
# while (pybullet.isConnected()):
#     pybullet.stepSimulation()