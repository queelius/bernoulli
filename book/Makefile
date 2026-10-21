TEX = pdflatex
TEXFLAGS = -interaction=nonstopmode -halt-on-error
BIB = biber
IDX = makeindex
MAIN = book

.PHONY: all build draft html watch clean cleanall

all: build

build:
	$(TEX) $(TEXFLAGS) $(MAIN).tex
	$(BIB) $(MAIN)
	$(IDX) -s $(MAIN).ist $(MAIN).idx
	$(TEX) $(TEXFLAGS) $(MAIN).tex
	$(IDX) -s $(MAIN).ist $(MAIN).idx
	$(TEX) $(TEXFLAGS) $(MAIN).tex

draft:
	$(TEX) $(TEXFLAGS) $(MAIN).tex

# Browsable HTML (make4ht in MathJax mode) for metafunctor.com. Reuses the PDF
# build's bibliography and index; tools/mathjax_macros.py teaches MathJax the
# book's macros and fails if math uses a macro it cannot define.
HTML_BUILD = _html_build
HTML_OUT = _html

HTML_SOURCES = $(MAIN).tex preamble.tex alex.sty references.bib $(MAIN).ist \
               frontmatter parts chapters appendices figures

html: build
	rm -rf $(HTML_BUILD) $(HTML_OUT) && mkdir -p $(HTML_BUILD)
	cp -r $(HTML_SOURCES) $(MAIN).bbl $(MAIN).ind $(HTML_BUILD)/
	cd $(HTML_BUILD) && make4ht -u -d ../$(HTML_OUT) $(MAIN).tex "mathjax"
	python3 tools/mathjax_macros.py $(HTML_OUT)/$(MAIN).html alex.sty preamble.tex \
	  $$(find frontmatter parts chapters appendices -name '*.tex' | sort) --check \
	  --title="Bernoulli Types: Two-Sided Error in Approximate Membership, Retrieval, and Computation"

watch:
	@command -v inotifywait >/dev/null 2>&1 || { \
	  echo "inotifywait not found. Install inotify-tools."; exit 1; }
	while true; do \
	  inotifywait -e modify,create,delete -r . --exclude '\.(aux|log|pdf|toc|out|bbl|blg)$$' ; \
	  $(MAKE) draft ; \
	done

clean:
	rm -f *.aux *.log *.out *.toc *.lof *.lot *.bbl *.blg \
	      *.idx *.ind *.ilg *.synctex.gz *.fls *.fdb_latexmk \
	      *.glo *.gls *.glg \
	      *.bcf *.run.xml *-blx.bib
	rm -rf _minted-* $(HTML_BUILD) $(HTML_OUT)
	find frontmatter parts chapters appendices -name '*.aux' -delete 2>/dev/null || true

cleanall: clean
	rm -f $(MAIN).pdf
