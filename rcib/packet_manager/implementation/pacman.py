from rcib.packet_manager.packet_manager_adaptor import PacketManagerAdaptor
from rcib.packet_manager.packet import Packet
import re
from typing import List


class PacmanPacketManager(PacketManagerAdaptor):
    def __init__(self, name='pacman'):
        super().__init__()
        installed = '[i][installed][s]?'
        self.util_name = name
        self.install_prefix = '-S'
        self.install_suffix = '--noconfirm'
        self.delete_prefix = '-Rsn'
        self.delete_suffix = '--noconfirm'
        self.search_prefix = '-Ss'
        self.search_pattern = f'[r]/[n] [v] {installed} [o]? {installed}\n[D]'
        # pattern = '^([^\/]+)\/([^ ]+)\s*([^\s]+)\s*(?:\([^\)]+\))?\s*(\[installed\])?\n\s+([^\n]+)$'
        # self.regex = re.compile(pattern, re.MULTILINE)

    @property
    def supports_versioning(self) -> bool:
        return False

    def is_installed(self, packet: str) -> bool:
        return self._run_command('-Qk', packet)[0] == 0

    # def search(self, packet: str) -> List[Packet]:
        # search_result = self._run_command('-Ss', packet)[1]
        # packets = []
        # for result in self.regex.findall(search_result):
        # repository = result[0]
        # name = result[1]
        # version = result[2]
        # is_installed = len(result[3]) != 0
        # description = result[4]
        # packet = Packet(name, is_installed=is_installed, version=version,
        # repository=repository, description=description)
        # packets.append(packet)
        # return packets
