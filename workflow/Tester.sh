#!/usr/bin/env bash
set -e

echo "Activate it virtual enviroment  ~/.venv/bin/activate"
source ~/zephyrproject/.venv/bin/activate

echo "test Results"
python3 $1/workflow/testResults.py $2 $3 $4 $5 $6

echo "✅ tester run completed"
