PYTHON_INTERPRETER = python

test_environment:
	$(info >>> Checking Python evironment...)
	$(PYTHON_INTERPRETER) test_environment.py

requirements: test_environment
	$(info >>> Installing Python requirements...)
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt
