install-dependencies:
	pip install -r requirements.txt -r requirements-dev.txt

test:
	pytest --cov=src tests

typecheck:
	mypy --install-types --non-interactive --strict src