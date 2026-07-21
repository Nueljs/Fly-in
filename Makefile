.PHONY: install run debug clean lint lint-strict

MAP ?= maps/medium/01_dead_end_trap.txt

install:
	@echo "Installing dependencies..."
	pip install flake8 mypy

run:
	@echo "Running the simulation with map: $(MAP)"
	python3 main.py $(MAP)

debug:
	@echo "Starting debug mode with pdb on map: $(MAP)"
	python3 -m pdb main.py $(MAP)

run_visual:
	@echo "Running the visual simulation with map: $(MAP)"
	python3 main.py --visual $(MAP)

clean:
	@echo "Cleaning temporary files..."
	rm -rf __pycache__ .mypy_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +

lint:
	@echo "Running linter (flake8) and type checker (mypy)..."
	flake8 --exclude=.venv .
	mypy --exclude '\.venv' . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
