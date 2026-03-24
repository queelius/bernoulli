TEX      = pdflatex
BIB      = bibtex
MAIN     = main
TEXFLAGS = -interaction=nonstopmode -halt-on-error

SOURCES  = $(MAIN).tex defs.tex alex.sty references.bib \
           $(wildcard sections/*.tex) $(wildcard img/*.tex) \
           $(wildcard data/*.csv)

.PHONY: all draft clean cleanall watch wc sim help

all: $(MAIN).pdf  ## Build the paper (full: pdflatex + bibtex + 2x pdflatex)

$(MAIN).pdf: $(SOURCES)
	$(TEX) $(TEXFLAGS) $(MAIN)
	$(BIB) $(MAIN) || true
	$(TEX) $(TEXFLAGS) $(MAIN)
	$(TEX) $(TEXFLAGS) $(MAIN)

draft:  ## Single-pass build for quick iteration (no bibtex, no cross-refs)
	$(TEX) $(TEXFLAGS) $(MAIN)

clean:  ## Remove build artifacts (keep PDF)
	rm -f $(MAIN).aux $(MAIN).bbl $(MAIN).blg $(MAIN).log $(MAIN).out \
	      $(MAIN).toc $(MAIN).lof $(MAIN).lot $(MAIN).loa $(MAIN).acn \
	      $(MAIN).glo $(MAIN).ist $(MAIN).nlo $(MAIN).slo $(MAIN).fls \
	      $(MAIN).fdb_latexmk $(MAIN).synctex.gz \
	      sections/*.aux

cleanall: clean  ## Remove everything including the PDF
	rm -f $(MAIN).pdf

watch:  ## Rebuild on file changes (requires inotifywait)
	@which inotifywait > /dev/null 2>&1 || { echo "Install inotify-tools: sudo apt install inotify-tools"; exit 1; }
	@echo "Watching for changes... (Ctrl-C to stop)"
	@while true; do \
		inotifywait -qe modify $(SOURCES) 2>/dev/null; \
		echo "--- Rebuilding ---"; \
		$(MAKE) all; \
	done

wc:  ## Estimate word count (body text only, via texcount)
	@which texcount > /dev/null 2>&1 || { echo "Install texcount: sudo apt install texcount"; exit 1; }
	@texcount -inc -total $(MAIN).tex

sim:  ## Run Monte Carlo simulations
	python3 code/price_of_certainty.py --seed 42 --outdir data/

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | \
		awk -F ':.*## ' '{printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'
