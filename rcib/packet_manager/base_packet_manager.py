import abc

from typing import List, Union
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

    @abc.abstractmethod
    def install(self, packet: Union[Packet, str]) -> bool:
        pass

    @abc.abstractmethod
    def delete(self, packet: Union[Packet, str]) -> bool:
        pass

    @abc.abstractmethod
    def search(self, packet: Union[Packet, str]) -> List[Packet]:
        pass

    @abc.abstractmethod
    def local_search(self, packet: Union[Packet, str]) -> List[Packet]:
        pass

    @abc.abstractmethod
    def local_packages(self) -> List[Packet]:
        pass

    @abc.abstractmethod
    def version_of(self, packet: Union[Packet, str]) -> Version:
        pass

    @abc.abstractmethod
    def is_installed(self, packet: Union[Packet, str]) -> bool:
        pass
