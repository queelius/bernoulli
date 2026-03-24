# Design: Organize bernoulli_data_type as a Proper C++ Repository

**Date:** 2026-02-22
**Scope:** Structure only (no compilation fixes)

## Goals

1. Modern CMake header-only library layout
2. Unified Doxygen documentation (API + theory pages)
3. Clean git history starting from organized state
4. Private GitHub repo

## Directory Layout

```
bernoulli_data_type/
├── CMakeLists.txt
├── README.md
├── LICENSE
├── Doxyfile.in
├── .gitignore
│
├── include/
│   └── bernoulli/
│       ├── rate_span.hpp
│       ├── bernoulli_bool.hpp
│       ├── random_bernoulli_bool.hpp
│       ├── bernoulli_set.hpp
│       ├── bernoulli_set_concept.hpp
│       ├── bernoulli_set_perf.hpp
│       ├── bernoulli_set_expressions.hpp
│       ├── random_binary_perf.hpp
│       ├── bernoulli_map.hpp
│       ├── bernoulli_array.hpp
│       ├── bernoulli_value.hpp
│       ├── bloom_filter.hpp
│       ├── entropy_bloom_filter.hpp
│       ├── space_optimal_bloom_filter.hpp
│       ├── hash_set.hpp
│       ├── hash_set_builder.hpp
│       ├── hash_map.hpp
│       ├── hash_map_builder.hpp
│       ├── bool_coder.hpp
│       ├── bernoulli_relation.hpp
│       └── detail/
│           ├── hash_set_lvl2.hpp
│           ├── hash_set_lvl2_builder.hpp
│           ├── hash_map_lvl2.hpp
│           └── hash_map_lvl2_builder.hpp
│
├── docs/
│   ├── mainpage.md
│   └── pages/
│       ├── bernoulli_bool.md
│       ├── bernoulli_map.md
│       ├── bernoulli_model.md
│       ├── bernoulli_set.md
│       ├── codec.md
│       ├── noisy_logic.md
│       └── regular_type.md
│
├── tests/
│   ├── CMakeLists.txt
│   ├── test_hash_set.cpp
│   ├── test_hash_map.cpp
│   ├── test_bernoulli_relation.cpp
│   ├── test_bernoulli_value.cpp
│   └── utils.hpp
│
└── examples/
```

## File Migration Map

### Headers: code/include/ → include/bernoulli/

| Source | Destination |
|--------|-------------|
| `code/include/rate_span.hpp` | `include/bernoulli/rate_span.hpp` |
| `code/include/bernoulli_bool/bernoulli_boolean.hpp` | `include/bernoulli/bernoulli_bool.hpp` |
| `code/include/bernoulli_bool/random_bernoulli_boolean.hpp` | `include/bernoulli/random_bernoulli_bool.hpp` |
| `code/include/bernoulli_set/bernoulli_set.hpp` | `include/bernoulli/bernoulli_set.hpp` |
| `code/include/bernoulli_set/bernoulli_set_concept.hpp` | `include/bernoulli/bernoulli_set_concept.hpp` |
| `code/include/bernoulli_set/bernoulli_set_perf.hpp` | `include/bernoulli/bernoulli_set_perf.hpp` |
| `code/include/bernoulli_set/expressions/*.hpp` | `include/bernoulli/bernoulli_set_expressions.hpp` (consolidate) |
| `code/include/bernoulli_set/random_binary_performance_measures.hpp` | `include/bernoulli/random_binary_perf.hpp` |
| `code/include/bernoulli_map/bernoulli_map.hpp` | `include/bernoulli/bernoulli_map.hpp` (resolve conflict) |
| `code/include/bernoulli_array/bernoulli_array.hpp` | `include/bernoulli/bernoulli_array.hpp` |
| `code/include/bernoulli_value/zeroth_order_bernoulli.hpp` | `include/bernoulli/bernoulli_value.hpp` |
| `code/include/bloom_filter/bloom_filter.hpp` | `include/bernoulli/bloom_filter.hpp` |
| `code/include/bloom_filter/entropy_bloom_filter.hpp` | `include/bernoulli/entropy_bloom_filter.hpp` |
| `code/include/bloom_filter/space_optimal_bloom_filter.hpp` | `include/bernoulli/space_optimal_bloom_filter.hpp` |
| `code/include/hash_set/hash_set.hpp` | `include/bernoulli/hash_set.hpp` |
| `code/include/hash_set/hash_set_builder.hpp` | `include/bernoulli/hash_set_builder.hpp` |
| `code/include/hash_set/hash_set_lvl2.hpp` | `include/bernoulli/detail/hash_set_lvl2.hpp` |
| `code/include/hash_set/hash_set_lvl2_builder.hpp` | `include/bernoulli/detail/hash_set_lvl2_builder.hpp` |
| `code/include/hash_map/hash_map.hpp` | `include/bernoulli/hash_map.hpp` |
| `code/include/hash_map/hash_map_builder.hpp` | `include/bernoulli/hash_map_builder.hpp` |
| `code/include/hash_map/hash_map_lvl2.hpp` | `include/bernoulli/detail/hash_map_lvl2.hpp` |
| `code/include/hash_map/hash_map_lvl2_builder.hpp` | `include/bernoulli/detail/hash_map_lvl2_builder.hpp` |
| `code/include/coders/bool_coder.hpp` | `include/bernoulli/bool_coder.hpp` |
| `code/include/bernoulli_relation/reflexive_bernoulli_relation.hpp` | `include/bernoulli/bernoulli_relation.hpp` (combine) |
| `code/include/bernoulli_relation/symmetric_bernoulli_relation.hpp` | (merge into above) |

### Docs: root markdown → docs/pages/

| Source | Destination |
|--------|-------------|
| `BERNOULLI_BOOL.md` | `docs/pages/bernoulli_bool.md` |
| `BERNOULLI_MAP.md` | `docs/pages/bernoulli_map.md` |
| `BERNOULLI_MODEL.md` | `docs/pages/bernoulli_model.md` |
| `BERNOULLI_SET.md` | `docs/pages/bernoulli_set.md` |
| `CODEC.md` | `docs/pages/codec.md` |
| `NOISY_LOGIC.md` | `docs/pages/noisy_logic.md` |
| `REGULAR_TYPE_CONCEPT.md` | `docs/pages/regular_type.md` |
| `README.md` | `docs/mainpage.md` (adapted) + new `README.md` |

### Stray test files → tests/

| Source | Destination |
|--------|-------------|
| `code/include/bernoulli_relation/test.cpp` | `tests/test_bernoulli_relation.cpp` |
| `code/include/bernoulli_value/test.cpp` | `tests/test_bernoulli_value.cpp` |

### Files to Remove

- `docs/html/` — generated Doxygen HTML
- `docs/latex/` — generated Doxygen LaTeX
- `_site/` — generated Jekyll
- `_config.yml` — Jekyll config
- `plot_maj_vote.png` — stray image
- `tests/test_hash_set` — compiled binary
- `tests/compile_hash_map_test` — build script
- `tests/compile_hash_set_test` — build script
- `code/` — entire directory after migration

## CMake Design

```cmake
cmake_minimum_required(VERSION 3.14)
project(bernoulli_data_type VERSION 0.1.0 LANGUAGES CXX)

# Header-only INTERFACE library
add_library(bernoulli INTERFACE)
target_include_directories(bernoulli INTERFACE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>)
target_compile_features(bernoulli INTERFACE cxx_std_17)

# Doxygen documentation target
find_package(Doxygen)
if(DOXYGEN_FOUND)
    configure_file(Doxyfile.in Doxyfile @ONLY)
    add_custom_target(docs
        COMMAND ${DOXYGEN_EXECUTABLE} ${CMAKE_CURRENT_BINARY_DIR}/Doxyfile
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
endif()

# Tests (optional, disabled by default since code doesn't compile yet)
option(BUILD_TESTING "Build tests" OFF)
if(BUILD_TESTING)
    add_subdirectory(tests)
endif()
```

## Doxygen Configuration

- Convert existing `Doxyfile` to `Doxyfile.in`
- Key settings:
  - `INPUT = @PROJECT_SOURCE_DIR@/include @PROJECT_SOURCE_DIR@/docs`
  - `USE_MDFILE_AS_MAINPAGE = @PROJECT_SOURCE_DIR@/docs/mainpage.md`
  - `FILE_PATTERNS = *.hpp *.md`
  - `RECURSIVE = YES`
  - `OUTPUT_DIRECTORY = @CMAKE_CURRENT_BINARY_DIR@/docs`
  - `GENERATE_LATEX = NO` (can enable later)
  - `PROJECT_NAME = "Bernoulli Data Type"`
  - `PROJECT_BRIEF = "A Probabilistic Framework for Understanding and Constructing Approximate Data Types"`

## Merge Conflict Resolution

Keep the HEAD version of `bernoulli_map.hpp` (has per-element `error_rate(X const & x)` in addition to aggregate `error_rate()`).

## Git Setup

1. `git init`
2. Initial commit with organized structure
3. Create private GitHub repo via `gh repo create`
4. Push

## Non-Goals (for now)

- Fix compilation errors
- Modernize C++ (concepts, modules)
- CI/CD pipeline
- Package manager support (Conan, vcpkg)
- GitHub Pages deployment
