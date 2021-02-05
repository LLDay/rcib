from typing import List, Union, Tuple
from icecream import ic


class Version:
    def __init__(self, version: Union[int, str, List[Union[int, str]]] = ''):
        if isinstance(version, str):
            if len(version) == 0:
                self._version = []
            else:
                version = version.replace('-', '.')
                version = version.replace(':', '.')
                self._version = version.split('.')

        elif isinstance(version, int):
            self._version = [version]

        elif isinstance(version, list):
            self._version = version[:]

        elif isinstance(version, Version):
            self._version = version._version[:]

        else:
            raise TypeError("Wrong Version type")

        self._prepare_version()

    def _prepare_version(self):
        for i in range(len(self._version)):
            part = self._version[i]
            if isinstance(part, str) and part.isdigit():
                self._version[i] = int(part)

    def _allignment(self, other) -> Tuple[List, List]:
        this = Version(self)
        other = Version(other)

        if len(this._version) == 0 or len(other._version) == 0:
            return [], []

        max_size = max(
            map(len, (this._version, other._version)))

        this_len = len(this._version)
        other_len = len(other._version)

        this._version.extend([0] * (max_size - this_len))
        other._version.extend([0] * (max_size - other_len))

        return this._version, other._version

    def __eq__(self, other):
        try:
            this, other = self._allignment(other)
            return this == other
        except:
            return False

    def __gt__(self, other):
        try:
            this, other = self._allignment(other)
            return this > other
        except:
            return False

    def __str__(self):
        return '.'.join(str(v) for v in self._version)
