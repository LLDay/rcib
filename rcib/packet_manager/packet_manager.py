from rcib.utils import executable_exists
from .base_packet_manager import BasePacketManager
from .packet_manager_adaptor import PacketManagerAdaptor
from .version import Version
from .packet import Packet
from icecream import ic
from typing import List, Union, Optional

import rcib.packet_manager.implementation


class PacketManager(BasePacketManager):
    def __init__(self):
        self.available_managers = self.get_available_packet_managers()
        if len(self.available_managers) == 0:
            raise EnvironmentError("No available packet managers")

    def get_available_packet_managers(self) -> List[BasePacketManager]:
        pm_dict = {}
        for cls in PacketManagerAdaptor.__subclasses__():
            for name in cls.alias:
                pm_dict[name] = cls

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
        for i, pm in enumerate(self.available_managers):
            if pm.install(packet):
                self._swap(i)
                return True
        return False

    def delete(self, packet_name: str) -> bool:
        deleted = False
        for pm in self.available_managers:
            deleted = deleted or pm.delete(packet_name)
        return deleted

    def is_exists(self, packet: Packet) -> bool:
        for i in range(self.available_managers):
            if self.available_managers[i].is_exists(packet):
                self._swap(i)
                return True
        return False

    def is_installed(self, packet: Union[Packet, str]) -> bool:
        return any(am.is_installed(packet) for am in self.available_managers)

    def _common_search(self, packet: Union[Packet, str], attribute) -> List[Packet]:
        packet_name = packet if isinstance(packet, str) else packet.name
        all_packets = []
        for am in self.available_managers:
            search = getattr(am, attribute)(packet_name)
            if search:
                all_packets.extend(search)
        return all_packets

    def search(self, packet: Union[Packet, str]) -> List[Packet]:
        packet_name = packet if isinstance(packet, str) else packet.name
        all_packets = []
        for pm in self.available_managers:
            all_packets.extend(pm.search(packet_name))
        return all_packets

    def local_search(self, packet: Union[Packet, str]) -> List[Packet]:
        packet_name = packet if isinstance(packet, str) else packet.name
        all_packets = []
        for pm in self.available_managers:
            all_packets.extend(pm.local_search(packet_name))
        return all_packets

    def local_packages(self) -> List[Packet]:
        packets = []
        for pm in self.available_managers:
            packets.extend(pm.local_packages())
        return packets

    def version_of(self, packet: Union[Packet, str]) -> Optional[Version]:
        pass
