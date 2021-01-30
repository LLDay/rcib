from typing import List, Union, Tuple
from icecream import ic


class Version:
    def __init__(self, version: Union[int, str, List[Union[int, str]]]):
        if isinstance(version, str):
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
        this_version = Version(self)
        other_version = Version(other)
        max_size = max(
            map(len, (this_version._version, other_version._version)))

        this_len = len(this_version._version)
        other_len = len(other_version._version)

        this_version._version.extend([0] * (max_size - this_len))
        other_version._version.extend([0] * (max_size - other_len))

        return this_version._version, other_version._version

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
