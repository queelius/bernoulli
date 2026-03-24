# Bernoulli Data Type

A general framework for understanding and constructing approximate data types
with quantifiable error bounds. Traditional data types are wrapped in a
`bernoulli<T>` template that tracks error rates, enabling formal reasoning
about accuracy-space-time trade-offs.

> **Status:** Experimental. The code does not compile yet -- this is an
> active reorganization of older research code. The theory documentation
> is substantially more developed than the implementation.

## Key Ideas

- **Bernoulli Boolean** (`bernoulli<bool>`) -- a noisy Boolean with known
  error probability, the simplest case
- **Bernoulli Set** (`bernoulli<set<X>>`) -- approximate set membership;
  Bloom filters are a special case
- **Bernoulli Map** (`bernoulli<map<X,Y>>`) -- approximate functions;
  the most general type, can model any computable function with errors
- **Oblivious types** -- Bernoulli types whose error properties enable
  construction of oblivious programs

## Documentation

Theory documentation lives in `docs/pages/` and can be built with Doxygen:

- [Bernoulli Boolean](docs/pages/bernoulli_bool.md) -- the simplest Bernoulli type
- [Bernoulli Set](docs/pages/bernoulli_set.md) -- approximate sets
- [Bernoulli Map](docs/pages/bernoulli_map.md) -- approximate functions
- [Bernoulli Model](docs/pages/bernoulli_model.md) -- full theory
- [Codec](docs/pages/codec.md) -- encoding/decoding framework
- [Noisy Logic](docs/pages/noisy_logic.md) -- logic under noise
- [Regular Type](docs/pages/regular_type.md) -- why Bernoulli types aren't regular

## Building Documentation

```bash
cmake -S . -B build
cmake --build build --target docs
# Open build/docs/html/index.html
```

## Project Structure

```
include/bernoulli/     Header-only C++17 library
docs/pages/            Theory documentation (Doxygen pages)
tests/                 Tests (not functional yet)
examples/              Examples (empty, for future use)
```

## Using the Library

This is a header-only library. With CMake:

```cmake
add_subdirectory(bernoulli_data_type)
target_link_libraries(your_target PRIVATE bernoulli::bernoulli)
```

Then include headers:

```cpp
#include <bernoulli/bernoulli_set.hpp>
#include <bernoulli/bloom_filter.hpp>
```

## Author

Alexander Towell -- [metafunctor.com](https://metafunctor.com)

## License

MIT
