TEX = pdflatex
TEXFLAGS = -interaction=nonstopmode -halt-on-error
BIB = biber
MAIN = book

.PHONY: all build draft watch clean cleanall

all: build

build:
	$(TEX) $(TEXFLAGS) $(MAIN).tex
	-$(BIB) $(MAIN)
	$(TEX) $(TEXFLAGS) $(MAIN).tex
	$(TEX) $(TEXFLAGS) $(MAIN).tex

draft:
	$(TEX) $(TEXFLAGS) $(MAIN).tex

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
	      *.glo *.gls *.glg
	rm -rf _minted-*
	find frontmatter parts chapters appendices -name '*.aux' -delete 2>/dev/null || true

cleanall: clean
	rm -f $(MAIN).pdf
