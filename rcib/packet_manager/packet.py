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
        if not isinstance(other, Packet):
            return False
        names_are_equal = len(self.name) == 0 or len(
            other.name) == 0 or self.name == other.name
        return names_are_equal and self.version == other.version

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
