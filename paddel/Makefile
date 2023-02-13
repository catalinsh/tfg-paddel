lint:
	autoflake src --check --quiet
	isort src --check-only
	black src --check
	mypy src

format:
	autoflake src
	isort src
	black src