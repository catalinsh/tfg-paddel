LATEX_COMPILE = latexmk -cd -pdf
LATEX_CLEAN = $(LATEX_COMPILE) -bibtex-cond1 -c

memoria:
	$(LATEX_COMPILE) docs/memoria.tex

anexos:
	$(LATEX_COMPILE) docs/anexos.tex

docs: memoria anexos

docs-clean:
	$(LATEX_CLEAN) docs/memoria.tex
	$(LATEX_CLEAN) docs/anexos.tex
