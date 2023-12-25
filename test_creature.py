# contain tests for genome class

import unittest
import creature
import genome
import numpy as np


class TestCreature(unittest.TestCase):
    # def testCreatureExists(self):
    #     self.assertIsNotNone(creature.Creature)

    # def testCreatureGetFlatLinks(self):
    #     c = creature.Creature(gene_count=4)
    #     links = c.get_flat_links()
    #     self.assertEqual(len(links), 4)

    # def testExpLinks(self):
    #     c = creature.Creature(gene_count=4)
    #     links = c.get_flat_links()
    #     exp_links = c.get_expanded_links()
    #     self.assertGreaterEqual(len(exp_links), len(links))

    # def testToXML(self):
    #     c = creature.Creature(gene_count=4)
    #     c.get_expanded_links()
    #     xml_str = c.to_xml()
    #     with open('102.urdf', 'w') as f:
    #         f.write('<?xml version = "1.0"?>' + "\n" + xml_str)
    #     self.assertIsNotNone(xml_str)

    def testRadial(self):
        links = [
            genome.URDFLink(name="A", parent_name="None", recur=1),
            genome.URDFLink(name="B",
                            parent_name="A",
                            recur=2,
                            joint_origin_rpy_1=0.75,
                            link_length=1.0)
        ]
        c = creature.Creature(gene_count=2)
        c.flat_links = links
        c.get_expanded_links()
        xml_str = c.to_xml()
        with open('103.urdf', 'w') as f:
            f.write('<?xml version = "1.0"?>' + "\n" + xml_str)

    def testMotor(self):
        m = creature.Motor(0.1, 0.5, 0.5)
        self.assertIsNotNone(m)

    def testMotorValue(self):
        m = creature.Motor(0.1, 0.5, 0.5)
        self.assertEqual(m.get_output(), 1)

    def testMotorValue2(self):
        m = creature.Motor(0.1, 0.5, 0.5)
        m.get_output()
        m.get_output()
        m.get_output()
        self.assertGreater(m.get_output(), 0)

    def testCMot(self):
        c = creature.Creature(gene_count=4)
        ls = c.get_expanded_links()
        ms = c.get_motors()
        self.assertEqual(len(ls) - 1, len(ms))


unittest.main()
