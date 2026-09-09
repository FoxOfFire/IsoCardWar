#!/bin/bash

set -euo pipefail

SCRIPT_RET=0

echo "Running: black ."
if ! pyenv exec black . ; then
        SCRIPT_RET=1
fi

#echo "Running: autopep8 . -r --in-place"
#if ! pyenv exec autopep8 . -r --in-place ; then
#	SCRIPT_RET=1
#fi

echo "Running: vulture . --exclude '**/.pyenv/**','**/.venv/**' "
if ! vulture .  --exclude '**/.pyenv/**','**/.venv/**' ; then
	SCRIPT_RET=1
fi

echo "Running: flake8 --exclude=.venv,.pyenv ."
if ! pyenv exec flake8 --exclude=.venv,.pyenv . ; then
        SCRIPT_RET=1
fi

echo "Running: mypy . --exclude '(^|/)\.venv(/|$)' --exclude '(^|/)\.pyenv(/|$)'"
if ! pyenv exec mypy . --exclude '(^|/)\.venv(/|$)' --exclude '(^|/)\.pyenv(/|$)' ; then
        SCRIPT_RET=1
fi

echo "Running: isort . --skip .pyenv --skip .venv'"
if ! pyenv exec isort . --skip .pyenv --skip .venv; then
        SCRIPT_RET=1
fi

echo "Running: mdformat . "
if ! mdformat . ; then
	SCRIPT_RET=1
fi

echo "Running: mado check . "
if ! mado check . ; then
	SCRIPT_RET=1
fi

exit $SCRIPT_RET
