#!/bin/sh

WORKDIR=~/.cache/$(basename $(pwd))
PYTHON="$WORKDIR/.venv/bin/python" 
test -e $WORKDIR/.venv ||\
    /usr/bin/python3 -m venv $WORKDIR/.venv &&\
    $PYTHON -m pip install --upgrade pip &&\
    $PYTHON -m pip install -r $PWD/requirements.txt
