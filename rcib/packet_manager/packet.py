from typing import List, Union
from icecream import ic
from operator import itemgetter
import re


class Packet:
    def _parse_version(self, version: str) -> List[Union[str, int]]:
        if not isinstance(version, str):
            version = str(version)
        version = version.replace('-', '.')
        if version.find('.') < 0:
            if version.isdigit():
                return [int(version)]
            else:
                return [version]

        version_list: List[Union[str, int]] = []
        for part in version.split('.'):
            if part.isdigit():
                version_list.append(int(part))
            else:
                version_list.append(part)
        return version_list

    def _packet_from_pattern(self, pattern: str, parse: str):
        parse = parse.rstrip()
        pattern = pattern.replace('/', r'\/')
        pattern = pattern.replace('(', r'\(')
        pattern = pattern.replace(')', r'\)')
        pattern = re.sub('\\[(?!.\\])', r'\[', pattern)
        pattern = re.sub('(?<!\\[.)\\]', r'\]', pattern)

        word = r'([\-\\w\\d\[\].\(\)]+)'
        line = r'([^\n]+)'
        space = r'\\s*'

        all_marks = {'repository': '[r]', 'name': '[n]', 'version': '[v]',
                     'other': '[o]', 'installed': '[i]', 'description': '[d]'}

        pattern = re.sub(r'[ \t]+', space, pattern)
        pattern = re.sub('\n', space + '\n' + space, pattern)

        order = []
        lower = pattern.lower()
        for key, mark in all_marks.items():
            index = lower.find(mark)
            while index > -1:
                order.append([key, index])
                index = lower.find(mark, index + 1)

        order.sort(key=itemgetter(1))

        while pattern.find('[i]') >= 0:
            pattern = pattern.replace('[i]', '(', 1)
            pattern = pattern.replace('[s]', ')', 1)

        marks_list = list(s.replace('[', '\\[').replace(']', '\\]')
                          for s in all_marks.values())
        pattern = re.sub('|'.join(marks_list), word, pattern)
        pattern = re.sub('|'.join(marks_list).upper(), line, pattern)

        found = re.findall(pattern, parse)[0]
        if isinstance(found, str):
            found = [found]

        result = {}
        for key in all_marks:
            result[key] = ''

        for key, value in zip(map(itemgetter(0), order), found):
            if result[key]:
                result[key] += ' '
            result[key] += value

        result = {k: result[k].rstrip() for k in result}
        result['installed'] = True if result['installed'] else False

        for key, value in result.items():
            if value:
                self.__setattr__(key, value)

    def __init__(self, pattern="", parse="", name="", is_installed=False, version="", repository="", description=""):
        self.name = name
        self._version = self._parse_version(version)
        self.repository = repository
        self.description = description
        self.installed = is_installed

        if pattern and parse:
            self._packet_from_pattern(pattern, parse)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Packet):
            return False
        return self.name == other.name and self.version == other.version

    def __ne__(self, other) -> bool:
        if not isinstance(other, Packet):
            return False
        return self.name != other.name or self.version != other.version

    @property
    def version(self) -> List[Union[str, int]]:
        return self._version

    @version.setter
    def version(self, version: str):
        self._version = self._parse_version(version)

    def __str__(self):
        string = str()
        if self.repository:
            string += '{self.repository}/'
        string += f'{self.name} '
        string += '.'.join(str(v) for v in self.version)
        if self.installed:
            string += ' [installed]'
        string += '\n' + self.description
        return string
