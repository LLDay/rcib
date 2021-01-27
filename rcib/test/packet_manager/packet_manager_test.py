import rcib.packet_manager.packet as packet
import unittest
from icecream import ic


class PacketTest(unittest.TestCase):
    def test_parse(self):
        p = packet.Packet(pattern='[n] [v]', parse='name 1')
        self.assertEqual(p.name, 'name')
        self.assertEqual(p.version,  [1])

        p = packet.Packet(pattern='[n] [v]', parse='name 1.2-e48hf')
        self.assertEqual(p.name, 'name')
        self.assertEqual(p.version,  [1, 2, 'e48hf'])

        p = packet.Packet(pattern='[n] [n]', parse='name1 name2')
        self.assertEqual(p.name, 'name1 name2')

        p = packet.Packet(pattern='[N] [d] [o]',
                          parse='Long name \n description other')
        self.assertEqual(p.name, 'Long name')
        self.assertEqual(p.description, 'description')

        p = packet.Packet(pattern='[o] [N] [D]',
                          parse='other name \n full description')
        self.assertEqual(p.name, 'name')
        self.assertEqual(p.description, 'full description')

        p = packet.Packet(pattern='[r]/[n]', parse='repo/name')
        self.assertEqual(p.name, 'name')
        self.assertEqual(p.repository, 'repo')

        pattern = '[n] [o]? [i]installed[s]?'
        p = packet.Packet(pattern=pattern, parse='name')
        self.assertEqual(p.name, 'name')
        self.assertFalse(p.installed)

        p = packet.Packet(pattern=pattern, parse='name other')
        self.assertEqual(p.name, 'name')
        self.assertFalse(p.installed)

        p = packet.Packet(pattern=pattern, parse='name other installed')
        self.assertEqual(p.name, 'name')
        self.assertTrue(p.installed)

    def test_parse_combo(self):
        pattern = '[n] [v]? [i]i[s]?'
        p = packet.Packet(pattern=pattern, parse='name 1 i',
                          name='another name', version=2, repository='repo', is_installed=False)
        self.assertEqual(p.name, 'name')
        self.assertEqual(p.repository, 'repo')
        self.assertEqual(p.version, [1])
        self.assertTrue(p.installed)

        p = packet.Packet(pattern=pattern, parse='name',
                          name='another name', version=2, repository='repo', is_installed=True)
        self.assertEqual(p.name, 'name')
        self.assertEqual(p.repository, 'repo')
        self.assertEqual(p.version, [2])
        self.assertTrue(p.installed)

        p = packet.Packet(pattern=pattern, parse='name', is_installed=False)
        self.assertFalse(p.installed)

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
