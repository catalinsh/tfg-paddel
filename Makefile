# PYTHON

create_environment:
	-conda env create --prefix ./venv --file ./environment.yml

install_dependencies:
	pip install -r requirements.txt -r requirements-dev.txt

test:
	pytest --cov tests

typecheck:
	mypy --install-types --non-interactive --strict src

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
