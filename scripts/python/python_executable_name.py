# Using old version
from sys import exit
from subprocess import check_output
from platform import python_version

SCRIPT = '''
from platform import python_version
print(python_version())
'''

ALLOWED_VERSION = [3, 6, 0]
VERSIONS = ['', '3'] + ['3.' + str(v) for v in range(6, 10)]
NAMES = ['python', 'py']


def version_is_allowed():
    version = [int(v) for v in python_version().split('.')]
    return version >= ALLOWED_VERSION


def get_allowed_executable(echo=False):
    for name in NAMES:
        for version in VERSIONS:
            try:
                executable = name + version
                output = check_output([executable, '-c', SCRIPT])
                output = str(output, 'utf-8')
                python_version = [int(v) for v in output.strip().split('.')]
                if python_version >= ALLOWED_VERSION:
                    if echo:
                        print(executable)
                    return executable
            except:
                pass
    return str()


if __name__ == "__main__":
    if not get_allowed_executable(True):
        exit(1)
