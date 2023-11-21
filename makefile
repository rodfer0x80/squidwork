.PHONY: build run clean 

build:
	@echo "Building..."
	@./scripts/build.sh

run: build
	@echo "Running..."
	@./scripts/run.sh

clean:
	@echo "Cleaning..."
	@./scripts/clean.sh

