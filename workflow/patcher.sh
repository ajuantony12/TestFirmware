#!/usr/bin/env bash
set -e

echo "Activate it virtual enviroment  ~/.venv/bin/activate"
source ~/zephyrproject/.venv/bin/activate

echo "incrementing patch"
python3 $1/src/cfg/scripts/incrementPatch.py $1/app/cfg/template/cfg_template.h.j2 $1/app/cfg/buildCfg.h $1/app/cfg/buildCfg.h

echo "✅ New patch release created"
