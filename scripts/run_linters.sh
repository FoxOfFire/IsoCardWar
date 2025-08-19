#!/bin/bash

set -euo pipefail

SCRIPT_RET=0

echo "Running: black ."
if ! black . ; then
        SCRIPT_RET=1
fi

echo "Running: flake8 ."
if ! pyenv exec flake8 . ; then
        SCRIPT_RET=1
fi

echo "Running: mypy ."
if ! pyenv exec mypy . ; then
        SCRIPT_RET=1
fi

echo "Running: isort ."
if ! isort . ; then
        SCRIPT_RET=1
fi

exit $SCRIPT_RET
