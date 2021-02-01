import re
from typing import List
from operator import itemgetter
from icecream import ic
from rcib.packet_manager.packet import Packet


class Parser:
    def __init__(self):
        self.marks = {'repository': '[r]', 'name': '[n]', 'version': '[v]',
                      'installed': '[i]', 'description': '[d]', 'other': '[o]'}
        self.tree = []

    def __len__(self):
        return len(self.tree)

    def __getitem__(self, key):
        return self.tree[key]

    def __iter__(self):
        return self.tree.__iter__()

    def _marks_order(self, pattern: str) -> List[int]:
        order = []
        lower = pattern.lower()
        for key, mark in self.marks.items():
            index = lower.find(mark)
            while index > -1:
                order.append([key, index])
                index = lower.find(mark, index + 1)

        order.sort(key=itemgetter(1))
        return list(map(itemgetter(0), order))

    def _prepared_pattern(self, pattern: str) -> str:
        word = r'[ \t]*([:\-\\w\\d\[\].\(\)]+)'
        line = r'[ \t]*([^\n]+)'

        pattern = pattern.replace('/', r'\/')
        pattern = pattern.replace('(', r'\(')
        pattern = pattern.replace(')', r'\)')
        pattern = re.sub('\\[(?!.\\])', r'\[', pattern)
        pattern = re.sub('(?<!\\[.)\\]', r'\]', pattern)
        pattern = re.sub('[ \t]+', '', pattern)

        marks_list = list(s.replace('[', '\\[').replace(']', '\\]')
                          for s in self.marks.values())
        pattern = re.sub('|'.join(marks_list), word, pattern)
        pattern = re.sub('|'.join(marks_list).upper(), line, pattern)
        return pattern

    def parse(self, pattern: str, string: str, installed_sign=''):
        order = self._marks_order(pattern)
        pattern = self._prepared_pattern(pattern)
        found = re.findall(pattern, string.rstrip(), re.MULTILINE)

        if not found:
            raise ValueError("Wrong pattern or string")

        if isinstance(found, str):
            found = [found]

        for result in found:
            self.tree.append(dict())

            for key in self.marks:
                self.tree[-1][key] = str()

            for key, value in zip(order, result):
                if self.tree[-1][key]:
                    self.tree[-1][key] += ' '
                self.tree[-1][key] += value.rstrip()

            self.tree[-1]['installed'] = len(installed_sign) > 0 and self.tree[-1]['installed'].find(
                installed_sign) >= 0

    def to_packets(self) -> List[Packet]:
        return [Packet(**p) for p in self.tree]
