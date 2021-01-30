from rcib.utils import executable_exists
from .base_packet_manager import BasePacketManager
from .implementation.pacman import *
from .version import Version
from icecream import ic
from typing import List


class PacketManager(BasePacketManager):
    def __init__(self):
        self.available_managers = self.get_available_packet_managers()
        if len(self.available_managers) == 0:
            raise EnvironmentError("No available packet managers")

    def get_available_packet_managers(self) -> List[BasePacketManager]:
        pm_dict = {'pacman': PacmanPacketManager}
        pm_list = []

        for k in pm_dict:
            if executable_exists(k):
                pm_list.append(pm_dict[k](k))

        return pm_list

    def _swap(self, i):
        if i != 0:
            am = self.available_managers
            am[i], am[0] = am[0], am[i]

    @property
    def name(str) -> str:
        return self.available_managers[0].name

    @property
    def version(self) -> Version:
        return self.available_managers[0].version

    @property
    def supports_versioning(self) -> bool:
        return self.available_managers[0].supports_versioning

    def install(self, packet: Packet) -> bool:
        for i in range(self.available_managers):
            if self.available_managers[i].install(packet):
                self._swap(i)
                return True
        return False

    def delete(self, packet_name: str) -> bool:
        deleted = False
        for manager in self.available_managers:
            deleted = deleted or m.delete(packet_name)
        return deleted

    def is_exists(self, packet: Packet) -> bool:
        for i in range(self.available_managers):
            if self.available_managers[i].is_exists(packet):
                self._swap(i)
                return True
        return False

    def is_installed(self, packet: Packet) -> bool:
        return any(am.is_installed(packet) for am in self.available_managers)

    def search(self, packet_name: str) -> List[Packet]:
        all_packets = []
        for am in self.available_managers:
            all_packets.extend(am.search(packet_name))
        return all_packets
