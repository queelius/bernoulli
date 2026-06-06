# Repo Organization Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Reorganize bernoulli_data_type from a loose collection of files into a proper modern C++ header-only library with CMake, Doxygen, and clean git history.

**Architecture:** Modern CMake INTERFACE library with flat `include/bernoulli/` namespace directory, Doxygen configured via `Doxyfile.in` with CMake substitution, theory docs as Doxygen `@page` entries under `docs/pages/`.

**Tech Stack:** C++17, CMake 3.14+, Doxygen, git, GitHub CLI (`gh`)

**Design doc:** `docs/plans/2026-02-22-repo-organization-design.md`

**GitHub user:** `queelius` | **Email:** `lex@metafunctor.com` | **Name:** `Alexander Towell`

---

### Task 1: Create directory skeleton

**Files:**
- Create: `include/bernoulli/` directory
- Create: `include/bernoulli/detail/` directory
- Create: `docs/pages/` directory
- Create: `examples/` directory

**Step 1: Create all target directories**

```bash
mkdir -p include/bernoulli/detail docs/pages examples
```

**Step 2: Verify structure**

```bash
find include docs/pages examples -type d
```

Expected:
```
include
include/bernoulli
include/bernoulli/detail
docs/pages
examples
```

---

### Task 2: Migrate header files to include/bernoulli/

**Files:**
- Move: All `.hpp` files from `code/include/*/` to `include/bernoulli/`
- Move: `code/include/rate_span.hpp` to `include/bernoulli/rate_span.hpp`

**Step 1: Copy single-file headers with renaming**

```bash
# Root-level header
cp code/include/rate_span.hpp include/bernoulli/rate_span.hpp

# bernoulli_bool
cp code/include/bernoulli_bool/bernoulli_boolean.hpp include/bernoulli/bernoulli_bool.hpp
cp code/include/bernoulli_bool/random_bernoulli_boolean.hpp include/bernoulli/random_bernoulli_bool.hpp

# bernoulli_set (individual files, NOT expressions/)
cp code/include/bernoulli_set/bernoulli_set.hpp include/bernoulli/bernoulli_set.hpp
cp code/include/bernoulli_set/bernoulli_set_concept.hpp include/bernoulli/bernoulli_set_concept.hpp
cp code/include/bernoulli_set/bernoulli_set_perf.hpp include/bernoulli/bernoulli_set_perf.hpp
cp code/include/bernoulli_set/random_binary_performance_measures.hpp include/bernoulli/random_binary_perf.hpp

# bernoulli_array
cp code/include/bernoulli_array/bernoulli_array.hpp include/bernoulli/bernoulli_array.hpp

# bernoulli_value
cp code/include/bernoulli_value/zeroth_order_bernoulli.hpp include/bernoulli/bernoulli_value.hpp

# bloom_filter
cp code/include/bloom_filter/bloom_filter.hpp include/bernoulli/bloom_filter.hpp
cp code/include/bloom_filter/entropy_bloom_filter.hpp include/bernoulli/entropy_bloom_filter.hpp
cp code/include/bloom_filter/space_optimal_bloom_filter.hpp include/bernoulli/space_optimal_bloom_filter.hpp

# hash_set (public)
cp code/include/hash_set/hash_set.hpp include/bernoulli/hash_set.hpp
cp code/include/hash_set/hash_set_builder.hpp include/bernoulli/hash_set_builder.hpp

# hash_map (public)
cp code/include/hash_map/hash_map.hpp include/bernoulli/hash_map.hpp
cp code/include/hash_map/hash_map_builder.hpp include/bernoulli/hash_map_builder.hpp

# coders
cp code/include/coders/bool_coder.hpp include/bernoulli/bool_coder.hpp
```

**Step 2: Copy detail (internal) headers**

```bash
cp code/include/hash_set/hash_set_lvl2.hpp include/bernoulli/detail/hash_set_lvl2.hpp
cp code/include/hash_set/hash_set_lvl2_builder.hpp include/bernoulli/detail/hash_set_lvl2_builder.hpp
cp code/include/hash_map/hash_map_lvl2.hpp include/bernoulli/detail/hash_map_lvl2.hpp
cp code/include/hash_map/hash_map_lvl2_builder.hpp include/bernoulli/detail/hash_map_lvl2_builder.hpp
```

**Step 3: Verify all headers migrated**

```bash
find include/bernoulli -name '*.hpp' | sort
```

Expected: 21 `.hpp` files (17 public + 4 detail). The expression headers and relation headers are handled in the next tasks.

---

### Task 3: Consolidate bernoulli_set expression headers

**Files:**
- Read: `code/include/bernoulli_set/expressions/*.hpp` (8 files)
- Create: `include/bernoulli/bernoulli_set_expressions.hpp`

**Step 1: Create consolidated expressions header**

Read all 8 expression files and concatenate them into a single header. The file should:
- Start with `#pragma once`
- Include all 8 expression files' contents (minus individual `#pragma once` lines)
- Keep all content as-is (don't fix compilation errors)

```cpp
#pragma once

// Consolidated from code/include/bernoulli_set/expressions/

// --- bernoulli_set_expr.hpp ---
// [contents]

// --- bernoulli_set_complement_expr.hpp ---
// [contents]

// --- bernoulli_set_union_expr.hpp ---
// [contents]

// --- bernoulli_set_intersection_expr.hpp ---
// [contents]

// --- bernoulli_set_disjoint_union_expr.hpp ---
// [contents]

// --- bernoulli_set_cartesian_expr.hpp ---
// [contents]

// --- bernoulli_set_power_expr.hpp ---
// [contents]

// --- bernoulli_set_union_exp.hpp ---
// [contents]
```

**Step 2: Verify file exists and has content from all 8 sources**

```bash
wc -l include/bernoulli/bernoulli_set_expressions.hpp
grep -c '// ---' include/bernoulli/bernoulli_set_expressions.hpp
```

Expected: ~100+ lines, 8 section markers.

---

### Task 4: Combine bernoulli_relation headers

**Files:**
- Read: `code/include/bernoulli_relation/reflexive_bernoulli_relation.hpp`
- Read: `code/include/bernoulli_relation/symmetric_bernoulli_relation.hpp`
- Create: `include/bernoulli/bernoulli_relation.hpp`

**Step 1: Create combined relation header**

Combine both relation files into one. Keep all content as-is.

```cpp
#pragma once

#include <memory>

// --- Reflexive Bernoulli Relation ---
// [contents of reflexive_bernoulli_relation.hpp]

// --- Symmetric Bernoulli Relation ---
// [contents of symmetric_bernoulli_relation.hpp]
```

**Step 2: Verify**

```bash
grep -c 'struct' include/bernoulli/bernoulli_relation.hpp
```

Expected: 2 (one per relation type).

---

### Task 5: Resolve merge conflict in bernoulli_map.hpp

**Files:**
- Modify: `include/bernoulli/bernoulli_map.hpp`

**Step 1: Resolve the conflict**

The file at `include/bernoulli/bernoulli_map.hpp` (copied in Task 2) contains a git merge conflict. Keep the HEAD version (lines before `=======`) which has the more complete API with `error_rate(X const & x)`. Remove all conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`).

**Step 2: Verify no conflict markers remain**

```bash
grep -c '<<<<<<\|======\|>>>>>>' include/bernoulli/bernoulli_map.hpp
```

Expected: 0

---

### Task 6: Migrate documentation files

**Files:**
- Move: `BERNOULLI_BOOL.md` → `docs/pages/bernoulli_bool.md`
- Move: `BERNOULLI_MAP.md` → `docs/pages/bernoulli_map.md`
- Move: `BERNOULLI_MODEL.md` → `docs/pages/bernoulli_model.md`
- Move: `BERNOULLI_SET.md` → `docs/pages/bernoulli_set.md`
- Move: `CODEC.md` → `docs/pages/codec.md`
- Move: `NOISY_LOGIC.md` → `docs/pages/noisy_logic.md`
- Move: `REGULAR_TYPE_CONCEPT.md` → `docs/pages/regular_type.md`
- Create: `docs/mainpage.md`

**Step 1: Copy doc files and add Doxygen @page headers**

For each markdown file, prepend a Doxygen `@page` directive as the first line so Doxygen renders them as pages in the navigation tree. The format is:

```markdown
@page page_id Page Title

[original content]
```

The page IDs and titles:
- `bernoulli_bool.md`: `@page bernoulli_bool Bernoulli Boolean`
- `bernoulli_map.md`: `@page bernoulli_map Bernoulli Map`
- `bernoulli_model.md`: `@page bernoulli_model Bernoulli Model`
- `bernoulli_set.md`: `@page bernoulli_set Bernoulli Set`
- `codec.md`: `@page codec Codec`
- `noisy_logic.md`: `@page noisy_logic Noisy Logic`
- `regular_type.md`: `@page regular_type Regular Type Concept`

**Step 2: Create docs/mainpage.md**

Write a new main page that serves as the Doxygen landing page:

```markdown
@mainpage Bernoulli Data Type

A general framework for understanding and constructing approximate data types
with quantifiable error bounds.

## Overview

The Bernoulli data type concept provides a probabilistic framework where
traditional data types are wrapped in a `bernoulli<T>` template that tracks
error rates. This enables:

- **Approximate data structures** (Bloom filters as `bernoulli<set<X>>`)
- **Oblivious programs** via composition of oblivious data types
- **Formal error analysis** through algebraic operations on error rates

## Documentation Pages

- @subpage bernoulli_bool — The simplest Bernoulli type
- @subpage bernoulli_set — Bernoulli sets (Bloom filters as a special case)
- @subpage bernoulli_map — The most general type, modeling any computable function
- @subpage bernoulli_model — The full Bernoulli model theory
- @subpage codec — Codecs and the universal Bernoulli map constructor
- @subpage noisy_logic — Logic operations under noise
- @subpage regular_type — Why Bernoulli types fail the Regular Type concept

## Source Code

The library is header-only C++17 under `include/bernoulli/`.
```

**Step 3: Verify all docs exist**

```bash
ls docs/pages/ docs/mainpage.md
```

Expected: 7 page files + mainpage.md

---

### Task 7: Migrate test files

**Files:**
- Keep: `tests/test_hash_set.cpp`, `tests/test_hash_map.cpp`, `tests/utils.hpp`
- Move: `code/include/bernoulli_relation/test.cpp` → `tests/test_bernoulli_relation.cpp`
- Move: `code/include/bernoulli_value/test.cpp` → `tests/test_bernoulli_value.cpp`

**Step 1: Copy stray test files**

```bash
cp code/include/bernoulli_relation/test.cpp tests/test_bernoulli_relation.cpp
cp code/include/bernoulli_value/test.cpp tests/test_bernoulli_value.cpp
```

**Step 2: Verify**

```bash
ls tests/*.cpp tests/*.hpp
```

Expected: 4 `.cpp` files + 1 `.hpp` file.

---

### Task 8: Remove old/generated files

**Files:**
- Delete: `docs/html/` (generated Doxygen)
- Delete: `docs/latex/` (generated Doxygen)
- Delete: `_site/` (generated Jekyll)
- Delete: `_config.yml` (Jekyll config)
- Delete: `plot_maj_vote.png` (stray image)
- Delete: `tests/test_hash_set` (compiled binary)
- Delete: `tests/compile_hash_map_test` (build script)
- Delete: `tests/compile_hash_set_test` (build script)
- Delete: `code/` (entire old directory, after migration)
- Delete: Old root markdown files (after migration to docs/pages/)
- Delete: Old `Doxyfile` (will be replaced by `Doxyfile.in`)

**Step 1: Remove generated output**

```bash
rm -rf docs/html docs/latex _site
rm -f _config.yml plot_maj_vote.png
rm -f tests/test_hash_set tests/compile_hash_map_test tests/compile_hash_set_test
```

**Step 2: Remove old source tree (ONLY after verifying migration is complete)**

```bash
# Verify migration first
diff <(find code/include -name '*.hpp' | wc -l) <(echo "should be 0 uncovered")
# Then remove
rm -rf code/
```

**Step 3: Remove old root markdown files**

```bash
rm -f BERNOULLI_BOOL.md BERNOULLI_MAP.md BERNOULLI_MODEL.md BERNOULLI_SET.md
rm -f CODEC.md NOISY_LOGIC.md REGULAR_TYPE_CONCEPT.md
rm -f Doxyfile
```

**Step 4: Verify clean state**

```bash
ls -la
```

Expected: Only `CMakeLists.txt`, `Doxyfile.in`, `README.md`, `LICENSE`, `.gitignore`, `include/`, `docs/`, `tests/`, `examples/` remain at the root.

---

### Task 9: Write CMakeLists.txt

**Files:**
- Create: `CMakeLists.txt`
- Create: `tests/CMakeLists.txt`

**Step 1: Write top-level CMakeLists.txt**

```cmake
cmake_minimum_required(VERSION 3.14)
project(bernoulli_data_type
    VERSION 0.1.0
    DESCRIPTION "A probabilistic framework for approximate data types"
    LANGUAGES CXX)

# Header-only INTERFACE library
add_library(bernoulli INTERFACE)
add_library(bernoulli::bernoulli ALIAS bernoulli)

target_include_directories(bernoulli INTERFACE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>)

target_compile_features(bernoulli INTERFACE cxx_std_17)

# Doxygen documentation target
find_package(Doxygen QUIET)
if(DOXYGEN_FOUND)
    configure_file(Doxyfile.in Doxyfile @ONLY)
    add_custom_target(docs
        COMMAND ${DOXYGEN_EXECUTABLE} ${CMAKE_CURRENT_BINARY_DIR}/Doxyfile
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
        COMMENT "Generating API documentation with Doxygen")
endif()

# Tests (disabled by default — code does not compile yet)
option(BUILD_TESTING "Build tests" OFF)
if(BUILD_TESTING)
    enable_testing()
    add_subdirectory(tests)
endif()
```

**Step 2: Write tests/CMakeLists.txt**

```cmake
# Tests are not functional yet — code does not compile.
# This is a placeholder for when compilation is fixed.

# add_executable(test_hash_set test_hash_set.cpp)
# target_link_libraries(test_hash_set PRIVATE bernoulli::bernoulli)
# add_test(NAME test_hash_set COMMAND test_hash_set)
```

**Step 3: Verify CMake syntax**

```bash
cmake -S . -B build 2>&1 | head -20
```

Expected: Configures successfully (Doxygen found or not found is fine).

---

### Task 10: Write Doxyfile.in

**Files:**
- Create: `Doxyfile.in`

**Step 1: Write a clean Doxyfile.in**

Rather than converting the 2600-line default Doxyfile, write a minimal one that only sets non-default values. Doxygen uses sensible defaults for everything else.

```
# Doxyfile.in — configured by CMake

PROJECT_NAME           = "Bernoulli Data Type"
PROJECT_NUMBER         = @PROJECT_VERSION@
PROJECT_BRIEF          = "A Probabilistic Framework for Approximate Data Types"

OUTPUT_DIRECTORY       = @CMAKE_CURRENT_BINARY_DIR@/docs

INPUT                  = @PROJECT_SOURCE_DIR@/include \
                         @PROJECT_SOURCE_DIR@/docs
FILE_PATTERNS          = *.hpp *.md
RECURSIVE              = YES

USE_MDFILE_AS_MAINPAGE = @PROJECT_SOURCE_DIR@/docs/mainpage.md

EXTRACT_ALL            = YES
GENERATE_LATEX         = NO
HAVE_DOT               = YES

# Markdown support
MARKDOWN_SUPPORT       = YES
AUTOLINK_SUPPORT       = YES
```

**Step 2: Verify Doxyfile.in exists**

```bash
cat Doxyfile.in | head -5
```

Expected: First line is `# Doxyfile.in — configured by CMake`

---

### Task 11: Write .gitignore

**Files:**
- Modify: `.gitignore`

**Step 1: Replace .gitignore with a clean C++ project version**

```gitignore
# Build directories
build/
cmake-build-*/

# Generated documentation
docs/generated/

# IDE
.idea/
.vscode/
*.swp
*~

# Compiled objects
*.o
*.obj
*.a
*.so
*.dylib

# OS files
.DS_Store
Thumbs.db

# LaTeX artifacts
*.aux
*.bbl
*.blg
*.fls
*.idx
*.ilg
*.ind
*.log
*.out
*.toc
*.fdb_latexmk
*.synctex.gz
```

---

### Task 12: Write README.md

**Files:**
- Modify: `README.md`

**Step 1: Write a clean project README**

The README should be concise and point to Doxygen for details. Include:
- Project name and one-line description
- Status note (experimental, code doesn't compile yet)
- Quick overview of the Bernoulli type concept
- Directory structure
- Build instructions (CMake + Doxygen)
- Link to theory docs
- Author info

---

### Task 13: Write LICENSE

**Files:**
- Create: `LICENSE`

**Step 1: Ask user which license they want, then create it**

Default suggestion: MIT License with `Alexander Towell` and year `2026`.

---

### Task 14: Git init and initial commit

**Files:**
- Create: `.git/` (via `git init`)

**Step 1: Initialize git**

```bash
git init
```

**Step 2: Stage all files**

```bash
git add CMakeLists.txt Doxyfile.in README.md LICENSE .gitignore
git add include/ docs/ tests/ examples/
```

**Step 3: Create initial commit**

```bash
git commit -m "feat: organize as modern CMake header-only library

Reorganize bernoulli_data_type from loose files into proper C++ project:
- Modern CMake INTERFACE library with include/bernoulli/ namespace
- Doxygen documentation with theory pages and API docs
- Clean directory structure: include/, docs/, tests/, examples/

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 15: Create private GitHub repo and push

**Step 1: Create repo**

```bash
gh repo create queelius/bernoulli_data_type --private --source=. --description "A probabilistic framework for approximate data types with quantifiable error bounds"
```

**Step 2: Push**

```bash
git push -u origin main
```

**Step 3: Verify**

```bash
gh repo view queelius/bernoulli_data_type --json url -q .url
```

---

### Task 16: Verify Doxygen generates

**Step 1: Build docs**

```bash
cmake -S . -B build && cmake --build build --target docs
```

**Step 2: Verify output**

```bash
ls build/docs/html/index.html
```

Expected: File exists. Open in browser to spot-check if desired.

**Step 3: Commit any Doxyfile.in fixes if needed**

If Doxygen produces warnings about missing `@page` directives or bad paths, fix `Doxyfile.in` or the markdown files and amend the commit.
