from shutil import which
from os import X_OK


def executable_exists(name: str, path=None) -> bool:
    return which(name, mode=X_OK, path=path) is not None
