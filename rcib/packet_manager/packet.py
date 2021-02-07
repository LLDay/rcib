from typing import List, Union
from .version import Version
from enum import Enum
from icecream import ic


class PacketStatus(Enum):
    INSTALLED = 0,
    UNINSTALLED = 1,
    UNDEFINED = 2


class Packet:
    def __init__(self, name="", pm="", installed=PacketStatus.UNDEFINED, version="", repository="", description="", **kwargs):
        self.name = kwargs.get('name', name)
        self._version = Version(kwargs.get('version', version))
        self.repository = kwargs.get('repository', repository)
        self.description = kwargs.get('description', description)
        self.installed = kwargs.get('installed', installed)
        self.pm = kwargs.get('pm', pm)

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            other = Packet(name=other)

        if not isinstance(other, Packet):
            return False

        self_len = len(self.name)
        other_len = len(other.name)
        empty_version = Version()

        names_are_equal = self_len == 0 or other_len == 0 or self.name == other.name
        versions_are_equal = self.version == empty_version or other.version == empty_version or self.version == other.version
        return names_are_equal and versions_are_equal

    def __ne__(self, other) -> bool:
        if not isinstance(other, Packet):
            return False
        return self.name != other.name or self.version != other.version

    @property
    def version(self) -> Version:
        return self._version

    @version.setter
    def version(self, version: str):
        self._version = Version(version)

    def __str__(self):
        string = str()
        if self.repository:
            string += self.repository + '/'
        string += f'{self.name} '
        string += str(self._version)
        if self.installed == PacketStatus.INSTALLED:
            string += ' [installed]'
        string += '\n    ' + self.description
        return string
