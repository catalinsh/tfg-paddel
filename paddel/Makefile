install-dependencies:
	pip install -e .[dev]

test:
	pytest --cov

lint:
	mypy src
	black src tests --check
	isort src tests --check-only

format:
	black src tests
	isort src tests