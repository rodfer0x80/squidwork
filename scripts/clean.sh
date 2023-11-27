#!/bin/sh

WORKDIR=~/.cache/$(basename $(pwd))
rm -rf $WORKDIR/* $PWD/**/__pycache__ $PWD/**/*/__pycache__
