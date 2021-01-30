import abc

from typing import List
from .packet import Packet
from rcib.packet_manager.version import Version


class BasePacketManager(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def name(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def version(self) -> Version:
        pass

    @property
    @abc.abstractmethod
    def supports_versioning(self) -> bool:
        pass

    def preinstall_hook(self):
        pass

    @abc.abstractmethod
    def install(self, packet: Packet) -> bool:
        pass

    def postinstall_hook(self):
        pass

    def predelete_hook(self):
        pass

    @abc.abstractmethod
    def delete(self, packet_name: str) -> bool:
        pass

    def postdelete_hook(self):
        pass

    @abc.abstractmethod
    def is_exists(self, packet: Packet) -> bool:
        pass

    @abc.abstractmethod
    def is_installed(self, packet_name: str) -> bool:
        pass

    @abc.abstractmethod
    def search(self, packet_name: str) -> List[Packet]:
        pass
