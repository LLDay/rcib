#!/usr/bin/env bash

PREFIX=${1:-'.'}

source "$PREFIX/scripts/bash/install_requiered_packages.sh"

RCIB_PYTHON=$("$PREFIX/rcib/utils/executable_name.py")
$RCIB_PYTHON -m pip install -r "$PREFIX/requirements.txt"
