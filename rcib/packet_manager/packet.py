from typing import List, Union
from .version import Version


class Packet:
    def __init__(self, name="", pm="", installed=False, version="", repository="", description="", **kwargs):
        self.name = kwargs.get('name', name)
        self._version = Version(kwargs.get('version', version))
        self.repository = kwargs.get('repository', repository)
        self.description = kwargs.get('description', description)
        self.installed = kwargs.get('installed', installed)
        self.pm = kwargs.get('pm', pm)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Packet):
            return False
        return self.name == other.name and self.version == other.version

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
        if self.installed:
            string += ' [installed]'
        string += '\n    ' + self.description
        return string
