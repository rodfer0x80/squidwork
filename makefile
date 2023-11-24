#!make
include .env
export USER_EMAIL
export USER_EMAIL_PASSWD

.PHONY: build run clean

build:
	@echo "Building..."
	@./scripts/build.sh

run: build
	@echo "Running..."
	@USER_EMAIL=$(USER_EMAIL) USER_EMAIL_PASSWD=$(USER_EMAIL_PASSWD) ./scripts/run.sh

clean:
	@echo "Cleaning..."
	@./scripts/clean.sh
