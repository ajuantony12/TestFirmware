#!/usr/bin/env bash
set -e

echo "Updating package index..."
sudo apt-get update -y
sudo apt upgrade

echo "Installing build essentials (GCC, G++, Make)..."
sudo apt-get install -y build-essential
sudo apt install --no-install-recommends git cmake ninja-build gperf ccache dfu-util device-tree-compiler wget python3-dev python3-venv python3-tk xz-utils file make gcc gcc-multilib g++-multilib libsdl2-dev libmagic1

echo "Create a virtual environment"
python3 -m venv $1/.venv

echo "Activate it virtual enviroment  $1/.venv/bin/activate"
source $1/.venv/bin/activate

echo "Install zephyr packages package"
pip install -r $1/workflow/requirements.txt
cp -f $1/zephyrproject ~/zephyrproject
west zephyr-export
west packages pip --install
cd ~/zephyrproject/zephyr
west sdk install
cd $1

echo "✅ All compilers and tools installed!"
