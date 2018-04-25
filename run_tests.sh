#! /usr/bin/env sh
export PYTHONPATH="src:$PYTHONPATH"

python2 -m pytest tests $@
python3 -m pytest tests $@