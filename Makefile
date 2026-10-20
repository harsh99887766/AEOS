.PHONY: install format lint test run

install:
	python -m pip install -e ".[dev]"

format:
	ruff format src tests

lint:
	ruff check src tests

test:
	pytest

run:
	uvicorn aeos.main:app --reload
