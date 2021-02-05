from rcib.packet_manager.packet_manager import PacketManager
from rcib.packet_manager.implementation.pacman import Pacman
from rcib.utils import executable_exists
from icecream import ic
import unittest


class PacketManagerTest(unittest.TestCase):

    def test_search(self):
        programm = 'bat'
        pm = PacketManager()
        pm.delete(programm)

        self.assertFalse(pm.is_installed(programm))
        self.assertTrue(pm.install(programm))
        self.assertTrue(pm.is_installed(programm))
        self.assertTrue(pm.delete(programm))
        self.assertFalse(pm.is_installed(programm))
