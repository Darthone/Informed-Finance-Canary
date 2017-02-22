#!/usr/bin/env bash 
# change to directory of this script
cd "$(dirname "$0")"
source ../../venv/bin/activate
PYTHONPATH=../../:$PYTHONPATH python ./$1
