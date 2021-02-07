from .base_packet_manager import BasePacketManager
from .packet import Packet, PacketStatus
from .parser import Parser
from .version import Version
from typing import List, Tuple, Union
from icecream import ic

import subprocess
import pdb
import re


class PacketManagerAdaptor(BasePacketManager):
    def __init__(self):
        self.util_name = ''
        self.use_util_name_in_command = True

        self.install_prefix = ''
        self.install_suffix = ''

        self.delete_prefix = ''
        self.delete_suffix = ''

        self.pm_version_args = ''
        self.pm_version_pattern = None

        self.search_prefix = ''
        self.search_suffix = ''
        self.search_pattern = ''
        self.installed_sign = None

        self.local_search_prefix = ''
        self.local_search_suffix = ''
        self.local_search_pattern = None

        self.local_packages_args = ''
        self.local_packages_pattern = None

        self.packet_vesion_prefix = ''
        self.packet_version_suffix = ''
        self.packet_version_pattern = None

    def _run_command(self, *args) -> subprocess.CompletedProcess:
        use_name = self._specific_attribute('use_util_name_in_command')

        command = [self.name] if use_name else []
        for arg in args:
            command.extend(arg.split())

        result = subprocess.run(command, capture_output=True,
                                text=True, shell=False, check=False)
        result.stdout = result.stdout.rstrip()
        return result

    def _convert_to_packet(self, packet: Union[Packet, str]) -> Packet:
        if isinstance(packet, str):
            return Packet(name=packet)
        return packet

    def _specific_attribute(self, attribute: str):
        specific_attribute = self.name + '_' + attribute
        return getattr(self, specific_attribute) if hasattr(self, specific_attribute) else getattr(self, attribute)

    def _parsed_packets(self, pattern, *args) -> List[Packet]:
        installed_sign = self._specific_attribute('installed_sign')
        result = self._run_command(*args)
        if result.returncode == 0:
            parser = Parser()
            parser.parse(pattern, result.stdout, installed_sign)
            packets = parser.to_packets()
            for packet in packets:
                packet.pm = self.name
            return packets
        return []

    @property
    def name(self) -> str:
        return self.util_name

    @property
    def version(self) -> Version:
        output = self._run_command(self.version_suffix)

    def install(self, packet: Union[Packet, str]) -> bool:
        packet = self._convert_to_packet(packet)
        result = self._run_command(
            self.install_prefix, packet.name, self.install_suffix)
        return result.returncode == 0

    def delete(self, packet: Union[Packet, str]) -> bool:
        packet = self._convert_to_packet(packet)
        result = self._run_command(
            self.delete_prefix, packet.name, self.delete_suffix)
        return result.returncode == 0

    def version_of(self, packet: Union[Packet, str]) -> Version:
        packet = self._convert_to_packet(packet)
        version_pattern = self._specific_attribute('version_pattern')
        packets = self._parsed_packets(
            version_pattern, self.packet_vesion_prefix, packet.name, self.packet_version_suffix)

        if len(packets) > 1:
            raise RuntimeError('Function must return one version')

        if len(packets) == 1:
            version = packets[0].version
            packet.verson = vesion
            return version
        return Version()

    def is_installed(self, packet: Union[Packet, str]) -> bool:
        packet = self._convert_to_packet(packet)
        if self.local_search_pattern is not None:
            packets = self.local_search(packet)
        else:
            packets = self.local_packages()

        for p in packets:
            if p == packet:
                packet.installed = p.installed
                return True
        return False

    def search(self, packet: Union[Packet, str]) -> List[Packet]:
        packet = self._convert_to_packet(packet)
        search_pattern = self._specific_attribute('search_pattern')
        return self._parsed_packets(search_pattern, self.search_prefix, packet.name, self.search_suffix)

    def local_search(self, packet: Union[Packet, str]) -> List[Packet]:
        packet = self._convert_to_packet(packet)
        search_pattern = self._specific_attribute('local_search_pattern')
        packets = self._parsed_packets(
            search_pattern, self.local_search_prefix, packet.name, self.local_search_suffix)

        for packet in packets:
            packet.installed = PacketStatus.INSTALLED

        return packets

    def local_packages(self) -> List[Packet]:
        pattern = self._specific_attribute('local_packages_pattern')
        if pattern is None:
            raise RuntimeError('Not specified pattern of local search')
        return self._parsed_packets(pattern, self.local_packages_args)
