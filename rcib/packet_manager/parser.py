import re
from typing import List
from operator import itemgetter
from icecream import ic


class Parser:
    def __init__(self):
        self.marks = {'repository': '[r]', 'name': '[n]', 'version': '[v]',
                      'other': '[o]', 'installed': '[i]', 'description': '[d]'}
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
        word = r'([\-\\w\\d\[\].\(\)]+)'
        line = r'([^\n]+)'
        space = r'\\s*'

        pattern = pattern.replace('/', r'\/')
        pattern = pattern.replace('(', r'\(')
        pattern = pattern.replace(')', r'\)')
        pattern = re.sub('\\[(?!.\\])', r'\[', pattern)
        pattern = re.sub('(?<!\\[.)\\]', r'\]', pattern)
        pattern = re.sub(r'[ \t]+', space, pattern)
        pattern = re.sub('\n+', space + '\n' + space, pattern)

        while pattern.find('[i]') >= 0:
            pattern = pattern.replace('[i]', '(', 1)
            pattern = pattern.replace('[s]', ')', 1)

        marks_list = list(s.replace('[', '\\[').replace(']', '\\]')
                          for s in self.marks.values())
        pattern = re.sub('|'.join(marks_list), word, pattern)
        pattern = re.sub('|'.join(marks_list).upper(), line, pattern)
        return pattern

    def parse(self, pattern: str, string: str):
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
                self.tree[-1][key] = ''

            for key, value in zip(order, result):
                if self.tree[-1][key]:
                    self.tree[-1][key] += ' '
                self.tree[-1][key] += value.rstrip()

            self.tree[-1]['installed'] = True if self.tree[-1]['installed'] else False
