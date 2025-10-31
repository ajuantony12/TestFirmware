#!/usr/bin/env bash
set -e

echo "Create a virtual environment"
python3 -m venv ~/zephyrproject/.venv

echo "Activate it virtual enviroment  ~/zephyrproject/.venv/bin/activate"
source ~/zephyrproject/.venv/bin/activate

echo "Install zephyr package packages package"
pip install -r $1/workflow/requirements.txt
# west init ~/zephyrproject
# cd ~/zephyrproject
# west sdk install
# cd $1
# Remove build directory if it exists
if [ -d "$1/build" ]; then
    echo "Removing existing build directory: $1/build"
    rm -rf "$1/build"
fi

echo "✅ All compilers and tools installed!"
