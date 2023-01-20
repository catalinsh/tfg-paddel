# PYTHON

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


# LATEX

LATEX_COMPILE = latexmk -cd -pdf
LATEX_CLEAN = $(LATEX_COMPILE) -bibtex-cond1 -c

memoria:
	$(LATEX_COMPILE) docs/memoria.tex

anexos:
	$(LATEX_COMPILE) docs/anexos.tex

docs: memoria anexos

docs_clean:
	$(LATEX_CLEAN) docs/memoria.tex
	$(LATEX_CLEAN) docs/anexos.tex
