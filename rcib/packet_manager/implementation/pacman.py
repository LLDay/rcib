from rcib.packet_manager.packet_manager_adaptor import PacketManagerAdaptor
from rcib.packet_manager.packet import Packet
import re
from typing import List


class Pacman(PacketManagerAdaptor):
    alias = ['pacman']

    def __init__(self, name: str):
        super().__init__()
        self.util_name = name
        self.install_prefix = '-S'
        self.install_suffix = '--noconfirm'
        self.delete_prefix = '-Rsn'
        self.delete_suffix = '--noconfirm'
        self.search_prefix = '-Ss'
        self.search_pattern = f'[r]/[n] [v] [O]? \n [D]'
        self.search_installed_sign = '[installed]'

    @property
    def supports_versioning(self) -> bool:
        return False

    def is_installed(self, packet: str) -> bool:
        return self._run_command('-Qk', packet)[0] == 0
