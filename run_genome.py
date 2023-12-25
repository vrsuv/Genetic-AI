import pybullet as p
import pybullet_data as pd
import creature
import genome as genlib
import time
import random
import numpy as np
import sys

def main(csv_file):
    p.connect(p.GUI)
    p.setPhysicsEngineParameter(enableFileCaching=0)
    p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
    plane_shape = p.createCollisionShape(p.GEOM_PLANE)
    floor = p.createMultiBody(plane_shape, plane_shape)
    p.setGravity(0, 0, -10)
    # p.setRealTimeSimulation(1)

    c = creature.Creature(gene_count=3)
    dna = genlib.Genome.from_csv('49_elite.csv')
    c.set_dna(dna)

    with open('test.urdf', 'w') as f:
        f.write(c.to_xml())
    rob1 = p.loadURDF('test.urdf')

    p.resetBasePositionAndOrientation(rob1, [0, 0, 3], [0, 0, 0, 1])
    start_pos, orn = p.getBasePositionAndOrientation(rob1)

    # iterate 
    elapsed_time = 0
    wait_time = 1.0/240 # seconds
    total_time = 10 # seconds
    step = 0
    while True:
        p.stepSimulation()
        step += 1
        if step % 24 == 0:
            motors = c.get_motors()
            assert len(motors) == p.getNumJoints(rob1), "Something went wrong"
            for jid in range(p.getNumJoints(rob1)):
                mode = p.VELOCITY_CONTROL
                vel = motors[jid].get_output()
                p.setJointMotorControl2(rob1, 
                            jid,  
                            controlMode=mode, 
                            targetVelocity=vel)
            new_pos, orn = p.getBasePositionAndOrientation(rob1)
            #print(new_pos)
            dist_moved = np.linalg.norm(np.asarray(start_pos) - np.asarray(new_pos))
            print(dist_moved)
        time.sleep(wait_time)
        elapsed_time += wait_time

        new_pos, orn = p.getBasePositionAndOrientation(rob1)
        # p.resetDebugVisualizerCamera(5, 0, 200, new_pos)
        if elapsed_time > total_time:
            break

    print("TOTAL DISTANCE MOVED:", dist_moved)

if __name__ == "__main__":
    assert len(sys.argv) == 2, "Usage: python playback_test.py csv_filename"
    main(sys.argv[1])


# p.connect(p.GUI)
# p.setPhysicsEngineParameter(enableFileCaching=0)
# p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
# plane_shape = p.createCollisionShape(p.GEOM_PLANE)
# floor = p.createMultiBody(plane_shape, plane_shape)
# p.setGravity(0, 0, -10)
# p.setRealTimeSimulation(1)

# c = creature.Creature(gene_count=3)
# dna = genlib.Genome.from_csv('49_elite.csv')
# c.set_dna(dna)

# with open('test.urdf', 'w') as f:
#     f.write(c.to_xml())
# rob1 = p.loadURDF('test.urdf')

# cid = p.loadURDF('test.urdf')
# p.setRealTimeSimulation(1)
# c.update_position([0, 0, 0])

# p.resetBasePositionAndOrientation(cid, [0, 0, 3], [0, 0, 0, 1])

# while True:
#     p.stepSimulation()  # mac
#     motors = c.get_motors()
#     assert len(motors) == p.getNumJoints(rob1), "Something went wrong"
#     for jid in range(p.getNumJoints(rob1)):
#         mode = p.VELOCITY_CONTROL
#         vel = 5 * (random.random() - 0.5)
#         p.setJointMotorControl2(rob1,
#                                 jid,
#                                 controlMode=mode,
#                                 targetVelocity=vel)

#     pos, orn = p.getBasePositionAndOrientation(cid)
#     c.update_position(pos)
#     print(c.get_distance_travelled())
#     time.sleep(0.004)
