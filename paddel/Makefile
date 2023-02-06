install-dependencies:
	pip install -e .[dev]

lint:
	autoflake src --check --quiet
	isort src --check-only
	black src --check
	mypy src --install-types

format:
	autoflake src
	isort src
	black src