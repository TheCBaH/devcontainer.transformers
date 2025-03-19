#!/bin/sh
set -e
set -x

echo "Activating feature 'pip_packages'"

PACKAGES=${PACKAGES:-$@}
echo "Selected packages: $PACKAGES"

python3 -m pip --no-cache-dir install $PACKAGES