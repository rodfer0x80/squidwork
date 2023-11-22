.PHONY: build run clean

build:
	./scripts/build.sh

run: build
	./scripts/run.sh

clean:
	./scripts/clean.sh
