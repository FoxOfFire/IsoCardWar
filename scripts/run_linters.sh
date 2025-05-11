#!/bin/bash

set -euo pipefail

SCRIPT_RET=0

echo "Running: black --check ."
if ! black --check . ; then
        SCRIPT_RET=1
fi

echo "Running: flake8 ."
if ! flake8 . ; then
        SCRIPT_RET=1
fi

echo "Running: mypy ."
if ! mypy . ; then
        SCRIPT_RET=1
fi

echo "Running: isort --check-only ."
if ! isort --check-only . ; then
        SCRIPT_RET=1
fi

exit $SCRIPT_RET
