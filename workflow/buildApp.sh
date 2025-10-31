#!/usr/bin/env bash
set -e

echo "Activate it virtual enviroment  ~/.venv/bin/activate"
source ~/zephyrproject/.venv/bin/activate

echo "Build application"
cd ~/zephyrproject/zephyr
west build -p always -build -d $1/build  -b b_u585i_iot02a $1/app
mv -f $1/build/zephyr/zephyr.elf $1/build/zephyr/viser-auto-tune.elf

cd $1



echo "✅ Build job finished!"
