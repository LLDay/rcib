from rcib.packet_manager.packet_manager_adaptor import PacketManagerAdaptor
from rcib.packet_manager.packet import Packet
import re
from typing import List


class Apt(PacketManagerAdaptor):
    alias = ['apt']

    def __init__(self, name: str):
        super().__init__()
        self.util_name = name
        self.use_util_name_in_command = False

        self.install_prefix = 'apt-get -y install'

        self.delete_prefix = 'apt-get -y purge'

        self.search_prefix = 'apt-cache --full search'
        self.search_pattern = 'Package: [N] [S] Version: [V] [S] Description: [D]'

        self.local_search_prefix = 'dpkg -l'
        self.local_search_pattern = 'ii [n] [v] [o] [D]'

        self.local_packages_args = self.local_search_prefix
        self.local_packages_pattern = self.local_search_pattern

    @property
    def supports_versioning(self) -> bool:
        return False
