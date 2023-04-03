LATEX_COMPILE = latexmk -cd -pdf
LATEX_CLEAN = $(LATEX_COMPILE) -bibtex-cond1 -c

.PHONY: memoria anexos

all: memoria anexos

memoria:
	$(LATEX_COMPILE) memoria.tex

anexos:
	$(LATEX_COMPILE) anexos.tex

clean:
	$(LATEX_CLEAN) memoria.tex
	$(LATEX_CLEAN) anexos.tex
