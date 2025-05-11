#!/bin/bash

set -euo pipefail

python -m venv .venv
.venv/bin/pip install -r requirements.txt
