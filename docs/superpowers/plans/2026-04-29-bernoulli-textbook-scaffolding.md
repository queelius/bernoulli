# Bernoulli Textbook: Repository Scaffolding Implementation Plan (Plan 0)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create `book/` (LaTeX) and `python/` (Python library) inside the `bernoulli/` monorepo with working build pipelines and passing smoke tests, ready to receive prose and code content in subsequent plans.

**Architecture:** Two new top-level subdirectories of the `bernoulli/` monorepo. `book/` holds LaTeX sources for a `book`-class document that compiles via `pdflatex` + `bibtex` to a single PDF. `python/` holds a teaching-oriented Python package using `hatchling` as build backend, with `pytest` smoke tests. Both are tracked in the monorepo as regular subdirectories. Migration of either to a standalone GitHub repo via `git subtree` is deferred to a future plan once content matures.

**Tech Stack:** LaTeX (book class), `pdflatex`, BibTeX, Make. Python 3.11+, `hatchling` (PEP 517 build backend), `pytest`, `numpy`, `sympy`. The notation package `alex.sty` is copied from `papers/bernoulli_sets/alex.sty` rather than re-derived. Bibliography style `alpha`.

**Scope:** Repository scaffolding only. Chapter prose, library implementation, and notebook content are out of scope for this plan and covered by later plans (Plan 1 onward).

---

## File Structure

After this plan completes, the following files exist in the repository:

```
bernoulli/
├── CLAUDE.md                                        # updated (now committed)
├── book/
│   ├── .gitignore                                   # LaTeX build artifacts
│   ├── README.md                                    # book repo overview
│   ├── LICENSE                                      # CC BY-NC-SA 4.0
│   ├── Makefile                                     # build/clean/watch targets
│   ├── book.tex                                     # document root
│   ├── preamble.tex                                 # \usepackage and macros
│   ├── alex.sty                                     # copy of papers/bernoulli_sets/alex.sty
│   ├── references.bib                               # placeholder bibliography (1 entry)
│   ├── frontmatter/
│   │   ├── titlepage.tex                            # title, author, date
│   │   ├── copyright.tex                            # license notice
│   │   └── preface.tex                              # prerequisites and reading guide (placeholder)
│   ├── parts/
│   │   ├── part1-atom.tex                           # \part + \input ch01..ch04
│   │   ├── part2-sets.tex                           # \part + \input ch05..ch08
│   │   ├── part3-maps.tex                           # \part + \input ch09..ch13
│   │   ├── part4-optimality.tex                     # \part + \input ch14..ch15
│   │   └── part5-boundary.tex                       # \part + \input ch16..ch18
│   ├── chapters/
│   │   ├── ch01-noisy-bit.tex                       # placeholder \chapter
│   │   ├── ch02-binary-channels.tex
│   │   ├── ch03-boolean-algebra-noise.tex
│   │   ├── ch04-axioms-kronecker.tex
│   │   ├── ch05-approximate-sets.tex
│   │   ├── ch06-set-composition.tex
│   │   ├── ch07-classification-measures.tex
│   │   ├── ch08-information-bounds.tex
│   │   ├── ch09-approximate-functions.tex
│   │   ├── ch10-sketches-estimators.tex
│   │   ├── ch11-randomized-algorithms.tex
│   │   ├── ch12-approximate-relations.tex
│   │   ├── ch13-algebra-types.tex
│   │   ├── ch14-optimal-bernoulli-sets.tex
│   │   ├── ch15-perfect-hash-filters.tex
│   │   ├── ch16-not-bernoulli.tex
│   │   ├── ch17-cipher-maps-trapdoor.tex
│   │   └── ch18-encrypted-search.tex
│   ├── appendices/
│   │   ├── A-probability-refresher.tex
│   │   ├── B-five-principles.tex
│   │   ├── C-library-walkthrough.tex
│   │   └── D-exercise-solutions.tex
│   ├── figures/
│   │   └── .gitkeep                                 # directory placeholder
│   └── code/
│       └── .gitkeep                                 # directory placeholder
└── python/
    ├── .gitignore                                   # python build artifacts
    ├── README.md                                    # library overview, tagline
    ├── LICENSE                                      # MIT
    ├── pyproject.toml                               # hatchling backend, pytest config
    ├── src/
    │   └── bernoulli/
    │       ├── __init__.py                          # public API exports, version
    │       ├── core.py                              # Bernoulli[T] placeholder
    │       └── py.typed                             # PEP 561 marker (empty file)
    ├── tests/
    │   ├── __init__.py                              # empty
    │   └── test_smoke.py                            # import + version + basic Bernoulli[T] tests
    └── notebooks/
        └── README.md                                # notebook conventions, one per book chapter
```

**Decomposition rationale:** `book/` is split into `frontmatter/`, `parts/`, `chapters/`, and `appendices/` so that each `\input{}` target has a single responsibility. `parts/partN-*.tex` files are thin wrappers (just `\part{...}` plus `\input{chapters/chXX-...}` lines) so part-level changes do not touch chapter files. `python/src/bernoulli/` follows the standard "src layout" so tests cannot accidentally import from the source tree without an install. `notebooks/` is a peer of `src/` and `tests/`, signaling that notebooks are first-class deliverables, not afterthoughts.

---

## Tasks

### Task 1: Verify build prerequisites are available

**Files:** none (environment check)

- [ ] **Step 1: Check pdflatex is installed**

Run: `which pdflatex && pdflatex --version | head -1`
Expected: prints a path and a version line starting with `pdfTeX 3.`

- [ ] **Step 2: Check Python 3.11+ is installed**

Run: `python3 --version`
Expected: `Python 3.11.x` or higher.

- [ ] **Step 3: Check pytest is available (or install it)**

Run: `python3 -m pytest --version`
Expected: prints pytest version. If absent, run `pip install --user pytest`.

- [ ] **Step 4: Check git is configured**

Run: `git config --get user.email`
Expected: prints `lex@metafunctor.com` or another configured email. (No commit needed for this task.)

---

### Task 2: Create `book/` directory and minimal compilable LaTeX

**Files:**
- Create: `book/.gitignore`
- Create: `book/book.tex`

- [ ] **Step 1: Create `book/.gitignore`**

Write `book/.gitignore` with:

```gitignore
# LaTeX build artifacts
*.aux
*.log
*.out
*.toc
*.lof
*.lot
*.bbl
*.blg
*.idx
*.ind
*.ilg
*.synctex.gz
*.fls
*.fdb_latexmk
_minted-*/
*.glo
*.gls
*.glg

# Final PDF is committed; intermediate PDFs are not
book.pdf.bak
```

- [ ] **Step 2: Create `book/book.tex` with minimal content**

Write `book/book.tex` with:

```latex
\documentclass[11pt,letterpaper,openright]{book}

\title{Bernoulli Types: An Algebra of Approximate Computation}
\author{Alexander Towell}
\date{\today}

\begin{document}
\maketitle
\tableofcontents

\chapter*{Placeholder}
This document compiles. Content will be added in subsequent plans.

\end{document}
```

- [ ] **Step 3: Verify the book builds**

Run: `cd book && pdflatex -interaction=nonstopmode book.tex`
Expected: compiles with warnings tolerable; `book/book.pdf` exists.

- [ ] **Step 4: Verify the PDF is non-empty**

Run: `ls -la book/book.pdf`
Expected: file size greater than 10 KB.

- [ ] **Step 5: Commit**

```bash
git add book/.gitignore book/book.tex
git commit -m "$(cat <<'EOF'
book: minimal compilable LaTeX scaffold

Adds book/book.tex with a placeholder chapter so the build pipeline can be
verified before content is added.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 3: Add `book/Makefile` with `build`, `draft`, `watch`, `clean`, `cleanall` targets

**Files:**
- Create: `book/Makefile`

- [ ] **Step 1: Write `book/Makefile`**

Write `book/Makefile` with:

```makefile
TEX = pdflatex
TEXFLAGS = -interaction=nonstopmode -halt-on-error
BIB = bibtex
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
```

- [ ] **Step 2: Verify `make` builds the book**

Run: `cd book && make`
Expected: PDF rebuilds successfully; exit code 0.

- [ ] **Step 3: Verify `make clean` keeps the PDF but removes auxiliaries**

Run: `cd book && make clean && ls book.pdf && ls *.aux 2>&1 | head -1`
Expected: `book.pdf` exists; aux files are gone (`ls: cannot access '*.aux'`).

- [ ] **Step 4: Verify `make cleanall` removes the PDF**

Run: `cd book && make cleanall && ls book.pdf 2>&1`
Expected: `ls: cannot access 'book.pdf': No such file or directory`.

- [ ] **Step 5: Rebuild for the next task**

Run: `cd book && make`
Expected: PDF builds cleanly.

- [ ] **Step 6: Commit**

```bash
git add book/Makefile
git commit -m "$(cat <<'EOF'
book: add Makefile with build/draft/watch/clean targets

build runs the full pdflatex+bibtex+pdflatex+pdflatex sequence. draft is a
single pass for fast iteration. watch rebuilds on file changes (requires
inotifywait). clean removes aux files but keeps the PDF; cleanall also
removes the PDF.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 4: Copy `alex.sty` notation package and add preamble

**Files:**
- Create: `book/alex.sty` (copied from `papers/bernoulli_sets/alex.sty`)
- Create: `book/preamble.tex`
- Modify: `book/book.tex`

- [ ] **Step 1: Copy `alex.sty` from papers**

Run: `cp papers/bernoulli_sets/alex.sty book/alex.sty`
Expected: file exists and is identical to the source.

Verify:

```bash
diff -q papers/bernoulli_sets/alex.sty book/alex.sty
```

Expected: no output (files identical).

- [ ] **Step 2: Write `book/preamble.tex`**

Write `book/preamble.tex` with:

```latex
% Notation package (unified macros: ASet, Set, fprate, fnrate, etc.)
\usepackage[fancy,section]{alex}

% Bibliography
\usepackage[backend=bibtex,style=alphabetic]{biblatex}
\addbibresource{references.bib}

% Hyperlinks
\usepackage[hidelinks,colorlinks=false]{hyperref}

% Better captions and floats
\usepackage{caption}
\usepackage{float}

% Code listings
\usepackage{listings}
\lstset{
  basicstyle=\ttfamily\small,
  breaklines=true,
  frame=single,
  numbers=left,
  numberstyle=\tiny,
  showstringspaces=false
}

% Theorem environments come from alex.sty
% Pseudocode
\usepackage{algorithm}
\usepackage{algpseudocode}

% Useful math packages not in alex.sty
\usepackage{bm}
```

- [ ] **Step 3: Modify `book/book.tex` to use the preamble**

Replace `book/book.tex` with:

```latex
\documentclass[11pt,letterpaper,openright]{book}

\input{preamble}

\title{Bernoulli Types: An Algebra of Approximate Computation}
\author{Alexander Towell}
\date{\today}

\begin{document}
\maketitle
\tableofcontents

\chapter*{Placeholder}
This document compiles with the \texttt{alex.sty} notation package loaded.
The approximate set notation \(\ASet{A}\) is available, as are the rate
macros \(\fprate\) and \(\fnrate\).

\end{document}
```

- [ ] **Step 4: Build and verify the macros render**

Run: `cd book && make cleanall && make`
Expected: PDF builds successfully; `\ASet{A}`, `\fprate`, `\fnrate` macros do not produce errors.

- [ ] **Step 5: Inspect the PDF for correct macro rendering**

Run: `cd book && grep -i "error\|undefined" book.log | head -20`
Expected: no "undefined control sequence" errors related to alex.sty macros.

- [ ] **Step 6: Commit**

```bash
git add book/alex.sty book/preamble.tex book/book.tex
git commit -m "$(cat <<'EOF'
book: add alex.sty notation package and preamble

Copy alex.sty from papers/bernoulli_sets/. Add preamble.tex loading
the package plus biblatex, hyperref, listings, algorithm. The book root
verifies macros render without error.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 5: Create frontmatter stubs (titlepage, copyright, preface)

**Files:**
- Create: `book/frontmatter/titlepage.tex`
- Create: `book/frontmatter/copyright.tex`
- Create: `book/frontmatter/preface.tex`
- Modify: `book/book.tex`

- [ ] **Step 1: Write `book/frontmatter/titlepage.tex`**

Write `book/frontmatter/titlepage.tex` with:

```latex
\begin{titlepage}
\centering
\vspace*{2in}

{\Huge\bfseries Bernoulli Types\par}
\vspace{0.5em}
{\Large\itshape An Algebra of Approximate Computation\par}

\vspace{2in}

{\Large Alexander Towell\par}
\vspace{0.5em}
{\large \today\par}

\vfill
\end{titlepage}
```

- [ ] **Step 2: Write `book/frontmatter/copyright.tex`**

Write `book/frontmatter/copyright.tex` with:

```latex
\thispagestyle{empty}
\vspace*{\fill}
\noindent
\textcopyright\ \the\year\ Alexander Towell.

\bigskip

\noindent
This work is licensed under a Creative Commons
Attribution-NonCommercial-ShareAlike 4.0 International License
(\url{https://creativecommons.org/licenses/by-nc-sa/4.0/}).

\bigskip

\noindent
The Python companion library \texttt{bernoulli} is released separately
under the MIT License.

\bigskip

\noindent
ORCID: \texttt{0000-0001-6443-9897}\\
Web: \url{https://metafunctor.com}\\
Source: \url{https://github.com/queelius/bernoulli-book}
\vspace*{\fill}
\clearpage
```

- [ ] **Step 3: Write `book/frontmatter/preface.tex`**

Write `book/frontmatter/preface.tex` with:

```latex
\chapter*{Preface}
\addcontentsline{toc}{chapter}{Preface}

This is a placeholder preface. The final preface will:

\begin{itemize}
  \item State the book's thesis and audience.
  \item Declare prerequisites: undergraduate probability, basic discrete
    math, comfort with proof, working Python knowledge for the notebook
    companion.
  \item Explain the lockstep notebook discipline (some chapters carry
    notebooks; theory-heavy chapters do not, by design).
  \item Provide a reading guide for the smart-undergrad-upward reader
    (chapters that admit a soft landing) and the adjacent-field grad
    student (the modal reader).
\end{itemize}
```

- [ ] **Step 4: Modify `book/book.tex` to include frontmatter**

Replace `book/book.tex` with:

```latex
\documentclass[11pt,letterpaper,openright]{book}

\input{preamble}

\begin{document}
\frontmatter

\input{frontmatter/titlepage}
\input{frontmatter/copyright}

\tableofcontents

\input{frontmatter/preface}

\mainmatter

\chapter*{Placeholder}
Parts and chapters will be \texttt{\textbackslash input}'d here in
subsequent tasks.

\backmatter
\end{document}
```

- [ ] **Step 5: Build and verify frontmatter renders**

Run: `cd book && make cleanall && make`
Expected: PDF builds; first three pages are titlepage / copyright / TOC; preface appears with chapter heading.

- [ ] **Step 6: Commit**

```bash
git add book/frontmatter book/book.tex
git commit -m "$(cat <<'EOF'
book: add frontmatter stubs (title, copyright, preface)

Title page uses the working title from the design spec. Copyright page
declares CC BY-NC-SA 4.0 for the prose and links to the MIT-licensed
Python companion. Preface is a placeholder marking what the final
preface will cover.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 6: Create 18 chapter stubs

**Files:**
- Create: `book/chapters/ch01-noisy-bit.tex` through `book/chapters/ch18-encrypted-search.tex`

- [ ] **Step 1: Write all 18 chapter stub files**

For each of the 18 chapters, create a file at `book/chapters/chXX-<slug>.tex` with the following template (substituting the actual title for each):

`book/chapters/ch01-noisy-bit.tex`:

```latex
\chapter{The Noisy Bit}
\label{ch:noisy-bit}

\textit{Placeholder. Content drafted in Plan 1.}
```

Repeat with these exact filenames and titles:

| File | Title |
|---|---|
| `ch01-noisy-bit.tex` | The Noisy Bit |
| `ch02-binary-channels.tex` | Binary Channels and Model Order |
| `ch03-boolean-algebra-noise.tex` | Boolean Algebra Under Noise |
| `ch04-axioms-kronecker.tex` | Two Axioms and Kronecker Factorization |
| `ch05-approximate-sets.tex` | Approximate Sets and Predicates |
| `ch06-set-composition.tex` | Composition of Sets |
| `ch07-classification-measures.tex` | Classification Measures |
| `ch08-information-bounds.tex` | Information-Theoretic Bounds |
| `ch09-approximate-functions.tex` | Approximate Functions and n-ary Channels |
| `ch10-sketches-estimators.tex` | Sketches and Estimators |
| `ch11-randomized-algorithms.tex` | Randomized Algorithms |
| `ch12-approximate-relations.tex` | Approximate Relations |
| `ch13-algebra-types.tex` | The Algebra of Approximate Types |
| `ch14-optimal-bernoulli-sets.tex` | Optimal Bernoulli Sets |
| `ch15-perfect-hash-filters.tex` | Perfect Hash Filters |
| `ch16-not-bernoulli.tex` | Approximate but Not Bernoulli |
| `ch17-cipher-maps-trapdoor.tex` | Cipher Maps and Trapdoor Computing |
| `ch18-encrypted-search.tex` | Encrypted Search as Relaxed Trapdoor |

Each file's body is exactly:

```latex
\chapter{<TITLE>}
\label{ch:<slug>}

\textit{Placeholder. Content drafted in <Plan N>.}
```

Use `<Plan 1>` for chapters 1-4, `<Plan 2>` for 5-8, `<Plan 3>` for 9-13, `<Plan 4>` for 14-18.

- [ ] **Step 2: Verify all 18 files exist**

Run: `ls book/chapters/ | wc -l`
Expected: `18`.

- [ ] **Step 3: Commit**

```bash
git add book/chapters
git commit -m "$(cat <<'EOF'
book: add 18 chapter stubs

Each chapter is a one-line placeholder pointing to the plan that will
draft it. Chapters 1-4: Plan 1 (Atom). 5-8: Plan 2 (Sets). 9-13: Plan 3
(Maps). 14-18: Plan 4 (Optimality and Boundary).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 7: Create 5 part files that input their chapters

**Files:**
- Create: `book/parts/part1-atom.tex` through `book/parts/part5-boundary.tex`

- [ ] **Step 1: Write `book/parts/part1-atom.tex`**

Write `book/parts/part1-atom.tex`:

```latex
\part{The Atom}

\input{chapters/ch01-noisy-bit}
\input{chapters/ch02-binary-channels}
\input{chapters/ch03-boolean-algebra-noise}
\input{chapters/ch04-axioms-kronecker}
```

- [ ] **Step 2: Write `book/parts/part2-sets.tex`**

```latex
\part{From Bits to Sets}

\input{chapters/ch05-approximate-sets}
\input{chapters/ch06-set-composition}
\input{chapters/ch07-classification-measures}
\input{chapters/ch08-information-bounds}
```

- [ ] **Step 3: Write `book/parts/part3-maps.tex`**

```latex
\part{From Sets to Maps}

\input{chapters/ch09-approximate-functions}
\input{chapters/ch10-sketches-estimators}
\input{chapters/ch11-randomized-algorithms}
\input{chapters/ch12-approximate-relations}
\input{chapters/ch13-algebra-types}
```

- [ ] **Step 4: Write `book/parts/part4-optimality.tex`**

```latex
\part{Optimality and Construction}

\input{chapters/ch14-optimal-bernoulli-sets}
\input{chapters/ch15-perfect-hash-filters}
```

- [ ] **Step 5: Write `book/parts/part5-boundary.tex`**

```latex
\part{The Boundary and Beyond}

\input{chapters/ch16-not-bernoulli}
\input{chapters/ch17-cipher-maps-trapdoor}
\input{chapters/ch18-encrypted-search}
```

- [ ] **Step 6: Modify `book/book.tex` to input the parts**

Replace `book/book.tex` with:

```latex
\documentclass[11pt,letterpaper,openright]{book}

\input{preamble}

\begin{document}
\frontmatter

\input{frontmatter/titlepage}
\input{frontmatter/copyright}

\tableofcontents

\input{frontmatter/preface}

\mainmatter

\input{parts/part1-atom}
\input{parts/part2-sets}
\input{parts/part3-maps}
\input{parts/part4-optimality}
\input{parts/part5-boundary}

\backmatter
\end{document}
```

- [ ] **Step 7: Build and verify the TOC has all parts and chapters**

Run: `cd book && make cleanall && make`
Expected: PDF rebuilds; TOC lists 5 parts and 18 chapters in order.

Verify TOC contents:

```bash
cd book && grep -c "chapter" book.toc
```

Expected: at least 18 (one entry per chapter; possibly more if subsections accrue).

- [ ] **Step 8: Commit**

```bash
git add book/parts book/book.tex
git commit -m "$(cat <<'EOF'
book: wire up 5 parts inputting their chapters

Each part file is a thin wrapper: \part heading plus \input lines for
its chapters. book.tex inputs all five parts in order. TOC now shows
the full 18-chapter structure.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 8: Create 4 appendix stubs

**Files:**
- Create: `book/appendices/A-probability-refresher.tex`
- Create: `book/appendices/B-five-principles.tex`
- Create: `book/appendices/C-library-walkthrough.tex`
- Create: `book/appendices/D-exercise-solutions.tex`
- Modify: `book/book.tex`

- [ ] **Step 1: Write each appendix stub**

`book/appendices/A-probability-refresher.tex`:

```latex
\chapter{Probability Refresher}
\label{app:probability}

\textit{Placeholder. Content drafted in Plan 5.}
```

`book/appendices/B-five-principles.tex`:

```latex
\chapter{The Five Core Principles}
\label{app:five-principles}

\textit{Placeholder. Cheat-sheet of the Two Axioms, Parametric Parsimony,
Space-Accuracy Duality, Composition Closure, and the Boolean Thread.
Content drafted in Plan 5.}
```

`book/appendices/C-library-walkthrough.tex`:

```latex
\chapter{Library Walkthrough}
\label{app:library}

\textit{Placeholder. Tour of the \texttt{bernoulli} Python package as a
unified entry point. Content drafted in Plan 5.}
```

`book/appendices/D-exercise-solutions.tex`:

```latex
\chapter{Selected Exercise Solutions}
\label{app:solutions}

\textit{Placeholder. Roughly half of the end-of-chapter exercises are
worked here; the rest are reader practice. Content drafted in Plan 5.}
```

- [ ] **Step 2: Modify `book/book.tex` to include the appendix**

Replace the `\backmatter` line with:

```latex
\appendix
\input{appendices/A-probability-refresher}
\input{appendices/B-five-principles}
\input{appendices/C-library-walkthrough}
\input{appendices/D-exercise-solutions}

\backmatter
```

The full updated `book/book.tex`:

```latex
\documentclass[11pt,letterpaper,openright]{book}

\input{preamble}

\begin{document}
\frontmatter

\input{frontmatter/titlepage}
\input{frontmatter/copyright}

\tableofcontents

\input{frontmatter/preface}

\mainmatter

\input{parts/part1-atom}
\input{parts/part2-sets}
\input{parts/part3-maps}
\input{parts/part4-optimality}
\input{parts/part5-boundary}

\appendix
\input{appendices/A-probability-refresher}
\input{appendices/B-five-principles}
\input{appendices/C-library-walkthrough}
\input{appendices/D-exercise-solutions}

\backmatter
\end{document}
```

- [ ] **Step 3: Build and verify appendices render**

Run: `cd book && make cleanall && make`
Expected: PDF rebuilds; appendices A-D appear after Part V in the TOC.

- [ ] **Step 4: Commit**

```bash
git add book/appendices book/book.tex
git commit -m "$(cat <<'EOF'
book: add 4 appendix stubs (probability, principles, library, solutions)

Appendix A is the probability refresher. B is the Five Core Principles
cheat sheet. C is the Python library walkthrough. D holds selected
exercise solutions. All are placeholders to be drafted in Plan 5.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 9: Add `references.bib` with one self-reference and verify bibtex pipeline

**Files:**
- Create: `book/references.bib`
- Modify: `book/chapters/ch01-noisy-bit.tex` (temporary citation, removed in Plan 1)

- [ ] **Step 1: Write `book/references.bib`**

Write `book/references.bib`:

```bibtex
@book{towell-bernoulli-book,
  author    = {Alexander Towell},
  title     = {Bernoulli Types: An Algebra of Approximate Computation},
  year      = {2026},
  publisher = {Self-published},
  note      = {Work in progress},
  url       = {https://github.com/queelius/bernoulli-book}
}

@misc{towell-bernoulli-sets,
  author = {Alexander Towell},
  title  = {Bernoulli sets: a model for random approximate sets},
  year   = {2026},
  note   = {Manuscript},
  howpublished = {\url{https://github.com/queelius/bernoulli_sets}}
}
```

- [ ] **Step 2: Add a temporary citation in chapter 1 to exercise the bibtex pipeline**

Edit `book/chapters/ch01-noisy-bit.tex` to:

```latex
\chapter{The Noisy Bit}
\label{ch:noisy-bit}

\textit{Placeholder. Content drafted in Plan 1.}
The framework appears in~\cite{towell-bernoulli-sets}.
```

- [ ] **Step 3: Build and verify bibtex resolves the citation**

Run: `cd book && make cleanall && make`
Expected: PDF rebuilds; chapter 1 shows a citation marker (e.g., `[Tow26]`); bibliography appears at the end of the book.

- [ ] **Step 4: Verify the bbl file exists**

Run: `ls book/book.bbl`
Expected: file exists.

- [ ] **Step 5: Verify bibtex log is clean**

Run: `grep -i "warning\|error" book/book.blg | head -10`
Expected: no errors. Warnings about missing fields are acceptable for now.

- [ ] **Step 6: Commit**

```bash
git add book/references.bib book/chapters/ch01-noisy-bit.tex
git commit -m "$(cat <<'EOF'
book: add references.bib and exercise the bibtex pipeline

Two placeholder entries in references.bib. Chapter 1 cites one of them
to verify pdflatex+bibtex+pdflatex+pdflatex produces a working bibliography.
The temporary citation in ch01 will be removed when content is drafted in
Plan 1.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 10: Add `book/figures/` and `book/code/` directory placeholders

**Files:**
- Create: `book/figures/.gitkeep`
- Create: `book/code/.gitkeep`

- [ ] **Step 1: Create empty placeholder files**

```bash
touch book/figures/.gitkeep book/code/.gitkeep
```

- [ ] **Step 2: Verify the directories exist**

```bash
ls -la book/figures/.gitkeep book/code/.gitkeep
```

Expected: both files exist (size 0 bytes).

- [ ] **Step 3: Commit**

```bash
git add book/figures/.gitkeep book/code/.gitkeep
git commit -m "$(cat <<'EOF'
book: add figures/ and code/ directory placeholders

figures/ will hold TikZ sources, PDF/PNG figures, and any external
graphics. code/ will hold extracted source listings for chapters
that include substantial code samples.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 11: Add `book/README.md` and `book/LICENSE`

**Files:**
- Create: `book/README.md`
- Create: `book/LICENSE`

- [ ] **Step 1: Write `book/README.md`**

Write `book/README.md`:

```markdown
# Bernoulli Types: An Algebra of Approximate Computation

A pedagogical monograph unifying probabilistic data structures, randomized
algorithms, noisy channels, and approximate functions under the Bernoulli
type framework.

> **Status:** scaffolding complete; chapter content in progress.

## Build

```bash
make            # full build (pdflatex + bibtex + pdflatex + pdflatex)
make draft      # single pdflatex pass (fast iteration; bibliography stale)
make watch      # rebuild on file changes (requires inotifywait)
make clean      # remove auxiliary files but keep the PDF
make cleanall   # remove everything including the PDF
```

The output is `book.pdf`.

## Structure

- `book.tex`: document root, inputs preamble and parts.
- `preamble.tex`: `\usepackage` calls and document-wide macros.
- `alex.sty`: unified notation package shared with the source papers.
- `frontmatter/`: title page, copyright, preface.
- `parts/`: five thin wrappers (`\part` plus `\input` chapters).
- `chapters/`: eighteen chapter sources.
- `appendices/`: probability refresher, principles cheat sheet, library walkthrough, selected solutions.
- `figures/`, `code/`: graphics and code listings.
- `references.bib`: bibliography.

## Companion Library

The Python library `bernoulli` lives at `../python/`. See its README for
installation and notebook conventions.

## Source Repositories

- Book sources: `https://github.com/queelius/bernoulli-book` (subtree push planned)
- Underlying papers: `https://github.com/queelius/bernoulli` (this monorepo)

## License

Prose: CC BY-NC-SA 4.0 (see `LICENSE`).
Code samples: MIT.

## Author

Alexander Towell, `lex@metafunctor.com`, ORCID `0000-0001-6443-9897`.
```

- [ ] **Step 2: Write `book/LICENSE` (CC BY-NC-SA 4.0 short notice)**

Write `book/LICENSE`:

```
Bernoulli Types: An Algebra of Approximate Computation
Copyright (c) 2026 Alexander Towell.

This work is licensed under the Creative Commons
Attribution-NonCommercial-ShareAlike 4.0 International License.

To view a copy of this license, visit:
https://creativecommons.org/licenses/by-nc-sa/4.0/

Source code embedded in the work (listings, examples, and the companion
Python package at ../python/) is dual-licensed under the MIT License.
```

- [ ] **Step 3: Commit**

```bash
git add book/README.md book/LICENSE
git commit -m "$(cat <<'EOF'
book: add README and LICENSE

README documents the build commands, structure, and companion library
location. LICENSE is the CC BY-NC-SA 4.0 short notice; embedded code
remains MIT.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 12: Initialize `python/` directory with `pyproject.toml`

**Files:**
- Create: `python/.gitignore`
- Create: `python/pyproject.toml`
- Create: `python/README.md`
- Create: `python/LICENSE`

- [ ] **Step 1: Write `python/.gitignore`**

Write `python/.gitignore`:

```gitignore
# Python build artifacts
__pycache__/
*.py[cod]
*$py.class
*.so
*.egg
*.egg-info/
.eggs/
build/
dist/
.tox/
.coverage
.coverage.*
htmlcov/
.pytest_cache/
.mypy_cache/
.ruff_cache/

# Virtual environments
.venv/
venv/
env/

# Jupyter
.ipynb_checkpoints/

# Editors
.vscode/
.idea/
*.swp
```

- [ ] **Step 2: Write `python/pyproject.toml`**

Write `python/pyproject.toml`:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "bernoulli"
version = "0.1.0"
description = "The type, not the data structure: random approximate types in Python"
readme = "README.md"
license = "MIT"
authors = [
  { name = "Alexander Towell", email = "lex@metafunctor.com" }
]
requires-python = ">=3.11"
keywords = [
  "bernoulli",
  "approximate-data-structures",
  "bloom-filter",
  "probabilistic-data-structures",
  "type-theory"
]
classifiers = [
  "Development Status :: 3 - Alpha",
  "Intended Audience :: Science/Research",
  "License :: OSI Approved :: MIT License",
  "Programming Language :: Python :: 3",
  "Programming Language :: Python :: 3.11",
  "Programming Language :: Python :: 3.12",
  "Topic :: Scientific/Engineering :: Mathematics",
  "Topic :: Software Development :: Libraries :: Python Modules"
]
dependencies = [
  "numpy >= 1.26",
  "sympy >= 1.13"
]

[project.optional-dependencies]
dev = [
  "pytest >= 8.0",
  "pytest-cov >= 5.0",
  "ruff >= 0.6",
  "mypy >= 1.10"
]
notebooks = [
  "jupyter >= 1.0",
  "matplotlib >= 3.8"
]

[project.urls]
Homepage = "https://github.com/queelius/bernoulli-py"
Documentation = "https://github.com/queelius/bernoulli-book"
Source = "https://github.com/queelius/bernoulli-py"
Issues = "https://github.com/queelius/bernoulli-py/issues"

[tool.hatch.build.targets.wheel]
packages = ["src/bernoulli"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.mypy]
python_version = "3.11"
strict = true
```

- [ ] **Step 3: Write `python/README.md`**

Write `python/README.md`:

```markdown
# bernoulli

> **The type, not the data structure.**

A teaching-oriented Python implementation of the Bernoulli framework for
random approximate types. Not a Bloom-filter package; a library for
tracking error rates through type composition.

## Status

Alpha. Public API and behavior may change.

## Install

```bash
pip install bernoulli
```

Or, from this repo:

```bash
pip install -e .
pip install -e ".[dev]"          # with development tooling
pip install -e ".[notebooks]"    # with Jupyter and matplotlib
```

## Quick Start

```python
from bernoulli import Bernoulli

# Placeholder API; full implementation coming in Plan 1+.
b = Bernoulli(value=True)
print(b.value)
```

## Notebooks

Notebooks live in `notebooks/`, paired chapter-by-chapter with the textbook
*Bernoulli Types: An Algebra of Approximate Computation* (`../book/`). Not
every chapter has a notebook; some are theory-only by design.

## Development

```bash
pytest                  # run smoke tests
ruff check src tests    # lint
mypy src                # type-check
```

## License

MIT. See `LICENSE`.

## Author

Alexander Towell, `lex@metafunctor.com`.
```

- [ ] **Step 4: Write `python/LICENSE` (MIT)**

Write `python/LICENSE`:

```
MIT License

Copyright (c) 2026 Alexander Towell

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 5: Commit**

```bash
git add python/.gitignore python/pyproject.toml python/README.md python/LICENSE
git commit -m "$(cat <<'EOF'
python: scaffold pyproject.toml, README, LICENSE

Hatchling build backend; numpy + sympy as runtime dependencies; pytest +
ruff + mypy as dev dependencies; jupyter + matplotlib as notebooks
extras. Tagline locked: "the type, not the data structure".

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 13: Write the failing smoke test for the Python package

**Files:**
- Create: `python/tests/__init__.py`
- Create: `python/tests/test_smoke.py`

- [ ] **Step 1: Create empty `python/tests/__init__.py`**

```bash
touch python/tests/__init__.py
```

- [ ] **Step 2: Write `python/tests/test_smoke.py`**

Write `python/tests/test_smoke.py`:

```python
"""Smoke tests verifying the bernoulli package imports and exposes a Bernoulli type."""

import importlib


def test_package_imports():
    """The bernoulli package must be importable."""
    bernoulli = importlib.import_module("bernoulli")
    assert bernoulli is not None


def test_version_string():
    """The package must expose a __version__ string."""
    import bernoulli
    assert hasattr(bernoulli, "__version__")
    assert isinstance(bernoulli.__version__, str)
    assert bernoulli.__version__ == "0.1.0"


def test_bernoulli_type_exists():
    """Bernoulli must be importable from the top-level package."""
    from bernoulli import Bernoulli
    assert Bernoulli is not None


def test_bernoulli_constructs_with_value():
    """Bernoulli(value=...) must accept a value and store it on .value."""
    from bernoulli import Bernoulli
    b = Bernoulli(value=True)
    assert b.value is True

    b2 = Bernoulli(value=42)
    assert b2.value == 42
```

- [ ] **Step 3: Run the test and verify it fails (no source yet)**

Run: `cd python && python -m pytest tests/test_smoke.py -v`
Expected: tests fail with `ModuleNotFoundError: No module named 'bernoulli'` (because the source module does not exist yet).

(No commit at this step. The test is committed together with its passing implementation in Task 14.)

---

### Task 14: Implement the minimal `bernoulli` package to make smoke tests pass

**Files:**
- Create: `python/src/bernoulli/__init__.py`
- Create: `python/src/bernoulli/core.py`
- Create: `python/src/bernoulli/py.typed`

- [ ] **Step 1: Create `python/src/bernoulli/py.typed` (PEP 561 marker)**

```bash
touch python/src/bernoulli/py.typed
```

- [ ] **Step 2: Write `python/src/bernoulli/core.py`**

Write `python/src/bernoulli/core.py`:

```python
"""Core types for the bernoulli package.

This module defines the Bernoulli[T] generic type, which wraps a value of
type T together with quantified error rates. The full implementation lands
in subsequent plans; this is a placeholder sufficient to make the package
import and the smoke tests pass.
"""

from typing import Generic, TypeVar

T = TypeVar("T")


class Bernoulli(Generic[T]):
    """A value of type T paired with quantified error rates.

    Parameters
    ----------
    value : T
        The wrapped value.

    Notes
    -----
    This is a placeholder. Future plans add error rate parameters,
    composition operators, and the algebra documented in the book.
    """

    def __init__(self, value: T) -> None:
        self.value: T = value
```

- [ ] **Step 3: Write `python/src/bernoulli/__init__.py`**

Write `python/src/bernoulli/__init__.py`:

```python
"""bernoulli: the type, not the data structure.

A Python library implementing the Bernoulli framework for random approximate
types. Companion to the textbook *Bernoulli Types: An Algebra of Approximate
Computation* by Alexander Towell.
"""

from bernoulli.core import Bernoulli

__version__ = "0.1.0"
__all__ = ["Bernoulli"]
```

- [ ] **Step 4: Install the package in editable mode**

Run: `cd python && pip install -e .`
Expected: installation succeeds; the `bernoulli` package is now importable in the active Python environment.

- [ ] **Step 5: Run the smoke tests and verify they pass**

Run: `cd python && python -m pytest tests/test_smoke.py -v`
Expected: all four tests pass:

```
tests/test_smoke.py::test_package_imports PASSED
tests/test_smoke.py::test_version_string PASSED
tests/test_smoke.py::test_bernoulli_type_exists PASSED
tests/test_smoke.py::test_bernoulli_constructs_with_value PASSED
```

- [ ] **Step 6: Commit**

```bash
git add python/src python/tests
git commit -m "$(cat <<'EOF'
python: implement minimal Bernoulli[T] placeholder + smoke tests

src/bernoulli/__init__.py exposes Bernoulli and __version__. core.py
defines Bernoulli as a Generic[T] placeholder with a single .value
attribute. Four smoke tests verify importability, version string, type
export, and value storage. Full Bernoulli[T] semantics arrive in Plan 1+.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 15: Add `python/notebooks/` directory with conventions README

**Files:**
- Create: `python/notebooks/README.md`

- [ ] **Step 1: Write `python/notebooks/README.md`**

Write `python/notebooks/README.md`:

```markdown
# Notebooks

This directory holds Jupyter notebooks paired with chapters of the textbook
*Bernoulli Types: An Algebra of Approximate Computation* (`../../book/`).

## Conventions

- One notebook per book chapter that has companion code.
- Filename pattern: `chXX-<short-topic>.ipynb` (matching the book's
  chapter source filenames in `book/chapters/`).
- Not every chapter has a notebook. Theory-heavy chapters (4, 13, 16, 17)
  are intentionally notebook-free; this is documented in the book preface.
- Each notebook starts with a markdown cell pointing back to the book
  section it accompanies and ends with cross-references to the next
  notebook in sequence.

## Running

```bash
pip install -e "..[notebooks]"
jupyter lab .
```

## Notebooks (planned)

Notebooks are added in subsequent plans alongside their chapters. The
expected set after all chapter plans complete:

| Chapter | Notebook | Plan |
|---|---|---|
| 1 | `ch01-noisy-bit.ipynb` | Plan 1 |
| 2 | `ch02-binary-channels.ipynb` | Plan 1 |
| 3 | `ch03-boolean-algebra-noise.ipynb` | Plan 1 |
| 5 | `ch05-approximate-sets.ipynb` | Plan 2 |
| 6 | `ch06-set-composition.ipynb` (light) | Plan 2 |
| 7 | `ch07-classification-measures.ipynb` | Plan 2 |
| 8 | `ch08-information-bounds.ipynb` (light) | Plan 2 |
| 9 | `ch09-approximate-functions.ipynb` | Plan 3 |
| 10 | `ch10-sketches-estimators.ipynb` | Plan 3 |
| 11 | `ch11-randomized-algorithms.ipynb` | Plan 3 |
| 12 | `ch12-approximate-relations.ipynb` | Plan 3 |
| 14 | `ch14-optimal-bernoulli-sets.ipynb` | Plan 4 |
| 15 | `ch15-perfect-hash-filters.ipynb` | Plan 4 |
| 16 | `ch16-not-bernoulli.ipynb` (light) | Plan 4 |
| 18 | `ch18-encrypted-search.ipynb` | Plan 4 |

Chapters 4, 13, 17 are theory-only.
```

- [ ] **Step 2: Commit**

```bash
git add python/notebooks/README.md
git commit -m "$(cat <<'EOF'
python: add notebooks/ directory with conventions README

Documents the one-notebook-per-chapter discipline (where natural) and
the planned notebook set. Theory chapters 4, 13, 17 are intentionally
notebook-free.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 16: Commit the existing top-level `CLAUDE.md` and update it for new subtrees

**Files:**
- Modify: `/home/spinoza/github/bernoulli/CLAUDE.md` (created earlier in this session, currently uncommitted)

- [ ] **Step 1: Verify the current state of `CLAUDE.md`**

Run: `git status -s CLAUDE.md`
Expected: `?? CLAUDE.md` (untracked).

Then read the file:

```bash
head -20 CLAUDE.md
```

Expected: starts with `# CLAUDE.md` and the standard guidance line.

- [ ] **Step 2: Append `book/` and `python/` rows to the routing table in `CLAUDE.md`**

Find the table that begins:

```
| Path | Role | Remote |
```

Replace the body of that table with:

```markdown
| `papers/` | 9 academic papers (LaTeX) plus a `pdf-archive/` of superseded drafts. Each paper is its own git subtree. | One remote *per paper* (see below) |
| `bernoulli-cpp/` | Header-only C++17 reference library (`bernoulli<T>` template, Bloom filter, perfect hash variants). Also a git subtree. | `bernoulli-cpp` |
| `book/` | Pedagogical monograph (LaTeX, book class) under active drafting. See `docs/superpowers/specs/2026-04-29-bernoulli-textbook-design.md`. | (subtree migration deferred) |
| `python/` | Teaching-oriented Python companion library (`bernoulli` package). | (subtree migration deferred) |
| `bernoulli_data_type.zip` | Legacy frozen archive of the original `bernoulli_data_type` repo before split. Do not edit. | (none) |
```

- [ ] **Step 3: Add a "Book and Library" routing line to the Routing section**

Find the section starting with `## Routing: Where to Start`. Add a new bullet after the existing ones:

```markdown
- **"Work on the textbook"** or **questions about chapter prose, the build, the Python companion library** → read `docs/superpowers/specs/2026-04-29-bernoulli-textbook-design.md` for the full design, then `book/README.md` and `python/README.md` for build commands.
```

- [ ] **Step 4: Verify the file still parses**

Run: `head -50 CLAUDE.md`
Expected: file is well-formed markdown; the new routing entry and table rows appear in their correct sections.

- [ ] **Step 5: Verify no soul-voice violations were introduced**

The repository runs a soul-voice hook on every write. Edits with banned phrases are blocked at write time, so this step is a sanity recheck against the staged diff:

```bash
git diff --cached CLAUDE.md | python3 -c "import sys; d=sys.stdin.read(); banned=[chr(0x2014), 'lever'+'age']; hits=[b for b in banned if b in d]; print('CLEAN' if not hits else f'FOUND: {hits}')"
```

Expected: `CLEAN`. If it reports `FOUND`, rewrite the offending text using commas, colons, periods, or parentheses, and rerun.

- [ ] **Step 6: Commit**

```bash
git add CLAUDE.md
git commit -m "$(cat <<'EOF'
Add top-level CLAUDE.md and document book/ and python/ subtrees

Top-level CLAUDE.md routes work between papers/, bernoulli-cpp/, book/,
and python/. Book and python rows note that subtree migration to standalone
GitHub repos is deferred until content matures.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 17: Final verification (full clean rebuild and test pass)

**Files:** none (verification only)

- [ ] **Step 1: Clean and rebuild the book**

Run: `cd book && make cleanall && make`
Expected: PDF builds with exit code 0; `book/book.pdf` exists.

- [ ] **Step 2: Verify the book PDF has the expected structure**

Run: `cd book && grep -E "^\\\\chapter|^\\\\part" book.toc | head -30`

Or if `book.toc` is not human-friendly, count chapter entries:

```bash
cd book && pdftotext book.pdf - | grep -c "^Chapter\|^Part"
```

Expected: at least 5 `Part` entries and 18 `Chapter` entries (plus 4 appendix chapters and the preface for ~28 total chapter-like entries).

- [ ] **Step 3: Run all Python tests**

Run: `cd python && python -m pytest -v`
Expected: 4 tests pass.

- [ ] **Step 4: Verify the Python package version matches**

Run: `python -c "import bernoulli; print(bernoulli.__version__)"`
Expected: `0.1.0`.

- [ ] **Step 5: Verify the working tree is clean**

Run: `git status -s`
Expected: empty output (no uncommitted changes), except possibly `M papers/CLAUDE.md` from before this plan (out of scope).

- [ ] **Step 6: Verify the commit log shows the expected scaffolding commits**

Run: `git log --oneline -20`
Expected: 16 new commits since the start of this plan, in roughly the order:

1. book: minimal compilable LaTeX scaffold
2. book: add Makefile
3. book: add alex.sty and preamble
4. book: add frontmatter stubs
5. book: add 18 chapter stubs
6. book: wire up 5 parts
7. book: add 4 appendix stubs
8. book: add references.bib and exercise the bibtex pipeline
9. book: add figures/ and code/ placeholders
10. book: add README and LICENSE
11. python: scaffold pyproject.toml, README, LICENSE
12. python: implement minimal Bernoulli[T] + smoke tests
13. python: add notebooks/ directory
14. Add top-level CLAUDE.md

(The exact count varies; verify the scaffolding deliverables exist rather than counting commits exactly.)

- [ ] **Step 7: Document completion**

No additional commit. The plan is complete when steps 1-6 of this task pass.

---

## Self-Review

**Spec coverage check.** Each spec section maps to plan task(s):

| Spec section | Tasks |
|---|---|
| §1 Purpose and Thesis | (deferred to chapter plans; scaffolding only here) |
| §2 Audience | Task 5 (preface placeholder) |
| §3 Format and Tone | Task 5 (preface), Task 11 (README) |
| §4 Through-Line: Atom Outward | Tasks 6-8 (TOC structure encodes atom-outward order) |
| §5 Structure: 5 Parts, 18 Chapters | Tasks 6, 7 |
| §6 Code Companion | Tasks 12-15 |
| §7 Tooling | Tasks 2-4 (LaTeX), 12-13 (Python) |
| §8 Citation Policy | Task 9 (references.bib) |
| §9 Repository Layout | All tasks; Task 16 documents in CLAUDE.md |
| §10 Prerequisites | Task 5 (preface placeholder mentions them) |
| §11 Exercises | Task 8 (Appendix D stub for solutions) |
| §12 Open Action Items | (deferred) |
| §13 Sequencing | This plan IS Plan 0 in the sequence |
| §14 Risks and Mitigations | Plan structure addresses "encyclopedic books don't get finished" risk via milestone decomposition |
| §15 Out of Scope | Each placeholder file makes scope explicit |
| §16 Success Criteria | Verified by Task 17 |

**Placeholder scan.** No "TBD", "TODO", "implement later" appear as plan-level placeholders. Some tasks DO create stub files containing the word "Placeholder" in the LaTeX text. These are intentional content placeholders for later plans, clearly labeled as such, and they are the deliverable of this plan. They are not plan failures.

**Type and naming consistency check.**
- `Bernoulli` class name used consistently across `core.py`, `__init__.py`, `tests/test_smoke.py`, and the README.
- File path `python/src/bernoulli/__init__.py` matches `pyproject.toml`'s `packages = ["src/bernoulli"]`.
- Chapter slugs (`ch01-noisy-bit`, etc.) match between Task 6 (creating files), Task 7 (parts inputting them), and Task 15 (notebooks README mapping).
- Part numbering (1-5) consistent throughout.

**Scope check.** This plan covers scaffolding only. Chapter prose, library implementation, and notebooks are explicitly out of scope and deferred to Plans 1-5 as documented in the spec §13.

**Ambiguity check.** "Editable install" in Task 14 assumes a Python environment is active; the plan's Task 1 step 3 verifies pytest is available, which implies a working Python environment. If the engineer is using a virtualenv they should activate it before Task 14 step 4.

---

## Plan complete

The plan is saved to `docs/superpowers/plans/2026-04-29-bernoulli-textbook-scaffolding.md`.

After this plan executes, the next plan to write is **Plan 1: Part I (Atom)**, drafting chapters 1-4 (~110 pp), at which point the book has a complete unification thesis fully expressed at the Boolean layer. Plan 1 should be written using `superpowers:writing-plans` after a separate `superpowers:brainstorming` session focused on Part I's chapter-by-chapter outline (the design spec covers Part I at the part level but does not yet outline section structure within chapters).
