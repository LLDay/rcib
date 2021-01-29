import rcib.packet_manager.packet as packet
import unittest
from icecream import ic


class PacketTest(unittest.TestCase):
    def get_packet(self, pattern: str, string: str) -> 'Packet':
        return packet.Packet.parsed_packets(pattern, string)[0]

    def test_parse(self):
        p = self.get_packet('[n] [v]', 'name 1')
        self.assertEqual(p.name, 'name')
        self.assertEqual(p.version,  [1])

        p = self.get_packet('[n] [v]', 'name 1.2-e48hf')
        self.assertEqual(p.name, 'name')
        self.assertEqual(p.version,  [1, 2, 'e48hf'])

        p = self.get_packet('[n] [n]', 'name1 name2')
        self.assertEqual(p.name, 'name1 name2')

        p = self.get_packet('[N] [d] [o]',
                            'Long name \n description other')
        self.assertEqual(p.name, 'Long name')
        self.assertEqual(p.description, 'description')

        p = self.get_packet('[o] [N] [D]',
                            'other name \n full description')
        self.assertEqual(p.name, 'name')
        self.assertEqual(p.description, 'full description')

        p = self.get_packet('[r]/[n]', 'repo/name')
        self.assertEqual(p.name, 'name')
        self.assertEqual(p.repository, 'repo')

        pattern = '[n] [o]? [i]installed[s]?'
        p = self.get_packet(pattern, 'name')
        self.assertEqual(p.name, 'name')
        self.assertFalse(p.installed)

        p = self.get_packet(pattern, 'name other')
        self.assertEqual(p.name, 'name')
        self.assertFalse(p.installed)

        p = self.get_packet(pattern, 'name other installed')
        self.assertEqual(p.name, 'name')
        self.assertTrue(p.installed)

    def test_comparing(self):
        p1 = packet.Packet(name='name', repository='repo', version='1.2.3')
        p2 = packet.Packet(name='other', repository='repo', version='1.2.3')
        p3 = packet.Packet(name='name', repository='repo', version='1.2.3.4')
        p4 = packet.Packet(name='name', version='1.2.3',
                           description='description')

        self.assertEqual(p1, p4)
        self.assertNotEqual(p1, p2)
        self.assertNotEqual(p1, p3)
        self.assertNotEqual(p2, p3)