#!/bin/sh

WORKDIR=~/.cache/$(basename $(pwd))
test -e $WORKDIR/.venv ||\
    /usr/bin/python3 -m venv $WORKDIR/.venv &&\
    $WORKDIR/.venv/bin/python -m pip install --upgrade pip &&\
    $WORKDIR/.venv/bin/python -m pip install -r $PWD/requirements.txt
