from python_executable_name import *
from subprocess import call
from sys import exit

python_name = get_allowed_executable()
command = python_name + ' -m tests'
call(command.split(), cwd='/vagrant')
