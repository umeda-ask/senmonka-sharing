#!/bin/bash
set -x

/opt/render/project/src/.venv/bin/python -m pip install --upgrade pip

pip install -r ./senmonka-sharing/requirements.txt
