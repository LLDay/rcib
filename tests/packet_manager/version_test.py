import unittest
from rcib.packet_manager.version import Version
from icecream import ic


class VersionTest(unittest.TestCase):
    def test_init(self):
        v = Version('1.2.3')
        self.assertEqual(v, [1, 2, 3])
        v = Version('34')
        self.assertEqual(v, 34)
        v = Version('1.2-4e3c')
        self.assertEqual(v, [1, 2, '4e3c'])

    def test_compare(self):
        v1 = Version('1.2.3')
        v2 = Version('1.2.3.4')
        v3 = Version('1.2.3-hefc')
        v4 = Version(2)
        v5 = Version('2.0')
        v6 = Version()

        self.assertGreater(v2, v1)
        self.assertGreater(v4, v1)
        self.assertGreater(v4, v2)
        self.assertNotEqual(v3, v2)
        self.assertEqual(v4, v5)

        for v in [v1, v2, v3, v4, v5, v6]:
            self.assertEqual(v6, v)
