import pybullet as p
import pybullet_data as pd
import creature
import genome
import time
import random 

p.connect(p.GUI)
p.setPhysicsEngineParameter(enableFileCaching=0)
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
plane_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(plane_shape, plane_shape)
p.setGravity(0, 0, -10)
p.setRealTimeSimulation(1)

c = creature.Creature(gene_count=3)
with open('test.urdf', 'w') as f:
    f.write(c.to_xml())
rob1 = p.loadURDF('test.urdf')

cid = p.loadURDF('test.urdf')
p.setRealTimeSimulation(1)
c.update_position([0, 0, 0])

p.resetBasePositionAndOrientation(cid, [0, 0, 3], [0, 0, 0, 1])

while True:
    p.stepSimulation()  # mac
    motors = c.get_motors()
    assert len(motors) == p.getNumJoints(rob1), "Something went wrong"
    for jid in range(p.getNumJoints(rob1)):
        mode = p.VELOCITY_CONTROL
        vel = 5 * (random.random() - 0.5)
        p.setJointMotorControl2(rob1,
                                jid,
                                controlMode=mode,
                                targetVelocity=vel)

    pos, orn = p.getBasePositionAndOrientation(cid)
    c.update_position(pos)
    # print(c.get_distance_travelled())
    time.sleep(0.004)
