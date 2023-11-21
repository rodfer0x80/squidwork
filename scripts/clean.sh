#!/bin/sh

WORKDIR="$XDG_CACHE_HOME/squidwork"
rm -rf $WORKDIR/* $PWD/**/__pycache__ $PWD/**/*/__pycache__
