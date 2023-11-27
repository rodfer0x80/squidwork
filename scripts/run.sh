#!/bin/sh

WORKDIR=~/.cache/$(basename $(pwd))
$WORKDIR/.venv/bin/python main.py
