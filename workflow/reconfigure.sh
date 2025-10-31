#!/usr/bin/env bash
set -e

echo "Activate it virtual enviroment  ~/.venv/bin/activate"
source ~/zephyrproject/.venv/bin/activate

echo "Install python packages package"
python3 $1/app/cfg/scripts/generateInputCfg.py $1/app/cfg/template/InputCfg_template.h.j2 $1/app/cfg/inputCfg.h $2

echo "✅ Reconfigured input"
