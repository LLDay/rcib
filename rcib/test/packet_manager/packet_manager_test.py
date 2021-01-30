from rcib.packet_manager.packet_manager import PacketManager
from icecream import ic
import unittest


class PacketManagerTest(unittest.TestCase):
    def test_search(self):
        packet_managers = PacketManager()
        for p in packet_managers.search('firefox'):
            print(p)
