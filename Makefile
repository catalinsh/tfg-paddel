PYTHON_INTERPRETER = python

test_environment:
	$(info >>> Checking Python evironment...)
	$(PYTHON_INTERPRETER) test_environment.py

requirements: test_environment
	$(info >>> Installing Python requirements...)
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

extract_landmarks: requirements
	$(info >>> Extracting landmarks from videos...)
	$(PYTHON_INTERPRETER) src/data/landmarkextraction.py data/raw data/landmarks
