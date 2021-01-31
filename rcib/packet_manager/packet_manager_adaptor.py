from .base_packet_manager import BasePacketManager
from .packet import Packet
from .parser import Parser
from .version import Version
from typing import List, Tuple
from subprocess import run, PIPE
from icecream import ic

import re


class PacketManagerAdaptor(BasePacketManager):
    def __init__(self):
        self.util_name = ''
        self.install_prefix = ''
        self.install_suffix = ''
        self.delete_prefix = ''
        self.delete_suffix = ''

        self.version_suffix = ''
        self.version_pattern = ''

        self.search_prefix = ''
        self.search_suffix = ''
        self.search_pattern = ''
        self.search_installed_sign = ''

        self.installed_prefix = ''
        self.installed_suffix = ''
        self.installed_pattern = ''

    def _run_command(self, *args) -> Tuple[int, List[str]]:
        command = [self.name]
        command.extend(args)
        result = run(command, capture_output=True,
                     text=True, shell=False, check=False)
        return result.returncode, result.stdout.rstrip()

    @property
    def name(self) -> str:
        return self.util_name

    @property
    def version(self) -> Version:
        output = self._run_command(self.version_suffix)

    def _install_call(self, packet_name: str) -> Tuple[int, List[str]]:
        return self._run_command(self.install_prefix, packet_name, self.install_suffix)

    def install(self, packet: Packet) -> bool:
        return self._install_call(packet.name)[0] == 0

    def _delete_call(self, packet_name: str) -> Tuple[int, List[str]]:
        return self._run_command(self.delete_prefix, packet_name, self.delete_suffix)

    def delete(self, packet_name: str) -> bool:
        return self._delete_call(packet_name)[0] == 0

    def is_exists(self, packet_name: str) -> bool:
        found_packets = self.search(packet_name)
        if packet_name in found_packets:
            return True
        return False

    def is_installed(self, packet_name: str):
        result = self._run_command(
            self.install_prefix, packet_name, self.install_suffix)

    def search(self, packet_name: str) -> List[Packet]:
        result = self._run_command(
            self.search_prefix, packet_name, self.search_suffix)
        if result[0] == 0:
            parser = Parser()
            parser.parse(self.search_pattern,
                         result[1], self.search_installed_sign)
            packets = parser.to_packets()
            for packet in packets:
                packet.pm = self.name
            return packets
