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
        self.search_pattern = '[r]/[n] [v] [I]?\n[D]'
        self.installed_sign = '[installed]'

        self.local_search_prefix = '-Qs'
        self.local_search_pattern = '[r]/[n] [v] [O]?\n[D]'

        self.local_packages_args = '-Qs'
        self.local_packages_pattern = '[r]/[n] [v] [O]?\n[D]'

    @property
    def supports_versioning(self) -> bool:
        return False
