# PYTHON
ENVIRONMENT_PREFIX = ./venv
ENVIRONMENT_FILE = ./environment.yml

create_environment:
	-conda env create --prefix $(ENVIRONMENT_PREFIX) --file $(ENVIRONMENT_FILE)

update_environment: create_environment
	conda env update --prefix $(ENVIRONMENT_PREFIX) --file $(ENVIRONMENT_FILE) --prune

test:
	tox -p

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
