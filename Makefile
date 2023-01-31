# Docker
docker-up:
	docker-compose up -d -t 0

docker-up-dev:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d -t 0

docker-restart:
	docker-compose restart -t 0

docker-down:
	docker-compose down -t 0

docker-clean:
	docker-compose down --rmi all -v -t 0


# Latex
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