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
