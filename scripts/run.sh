#!/bin/sh

WORKDIR=~/.cache/$(basename $(pwd))
PYTHON="$WORKDIR/.venv/bin/python3"
$PYTHON  main.py
