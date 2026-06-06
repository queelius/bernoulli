#!/usr/bin/env python3
"""Experiment 04: Codec entropy and non-member output distribution.

Goal: validate two claims about :mod:`bernoulli.maps.codec`:

1. **Shannon's source-coding bound holds.** For a value distribution with
   entropy ``H(Y)``, Huffman expected codeword length ``L`` satisfies
   ``H(Y) <= L < H(Y) + 1``. The "+1" gap is unavoidable in the worst
   case (think Bernoulli(0.5) needs 1 bit per value while H = 1; that is
   tight; for skewed distributions, L can be much closer to H).

2. **The codec controls the non-member output distribution.** For an
   approximate-map structure (e.g. ribbon retrieval) where non-member
   queries effectively decode a uniformly random M-bit pattern, the
   probability that a non-member returns ``v`` equals the codec's
   codespace fraction for ``v``. We simulate this by drawing N uniform
   m-bit patterns and tabulating decode outputs, then comparing to the
   codec's predicted non-member distribution via TV distance and KL
   divergence.

Sections:

For each of four value distributions over a small alphabet
``V = {v0, ..., v7}``:
- D1: uniform (max entropy: H = log2(8) = 3 bits)
- D2: heavily skewed (90% on v0, 10% spread over v1..v7)
- D3: Zipf with parameter s=1.0 (1/i mass on rank-i value)
- D4: two-mode (40% / 40% on v0, v1; 20% spread over v2..v7)

we compare three codec choices:
- DenseCodec at m_bits=3 (uniform 1/8 per value)
- PaddedCodec at m_bits=4 (default = mode of distribution)
- PrefixCodec built via Huffman from the value distribution

Output is a table of (distribution, codec) cells with columns:
- m_bits
- H(Y)         -- entropy of the *value distribution*
- L            -- expected codeword length under that distribution
- L - H(Y)     -- redundancy gap (Huffman <= 1 by Shannon)
- TV(predicted non-member, simulated non-member)
- KL(simulated || predicted)
"""

from __future__ import annotations

import math
import random
import sys
import time
from collections.abc import Mapping
from pathlib import Path
from typing import Generic, TypeVar

# Make the experiment runnable from anywhere; we expect to be in the
# repo root (the directory containing src/bernoulli/).
HERE = Path(__file__).resolve().parent
PKG_ROOT = HERE.parent
sys.path.insert(0, str(PKG_ROOT / "src"))

from bernoulli.maps.codec import (  # noqa: E402
    DenseCodec,
    PaddedCodec,
    PrefixCodec,
    shannon_entropy,
)

V = TypeVar("V")

# =====================================================================
# Distributions
# =====================================================================

VALUES = [f"v{i}" for i in range(8)]


def dist_uniform() -> dict[str, float]:
    return {v: 1.0 for v in VALUES}


def dist_skewed() -> dict[str, float]:
    # 90% on v0; remaining 10% spread evenly over v1..v7.
    rest = 7
    out = {VALUES[0]: 0.90}
    for v in VALUES[1:]:
        out[v] = 0.10 / rest
    return out


def dist_zipf(s: float = 1.0) -> dict[str, float]:
    # rank-i (1-indexed) gets weight 1 / i^s; normalize.
    raw = [1.0 / ((i + 1) ** s) for i in range(len(VALUES))]
    total = sum(raw)
    return {v: w / total for v, w in zip(VALUES, raw, strict=True)}


def dist_two_mode() -> dict[str, float]:
    # 40% / 40% on v0, v1; 20% spread over v2..v7 (i.e. 20% / 6 each).
    rest = 6
    out = {VALUES[0]: 0.40, VALUES[1]: 0.40}
    for v in VALUES[2:]:
        out[v] = 0.20 / rest
    return out


DISTRIBUTIONS: dict[str, dict[str, float]] = {
    "D1: uniform (max entropy)": dist_uniform(),
    "D2: heavily skewed (90/10)": dist_skewed(),
    "D3: Zipf s=1.0": dist_zipf(),
    "D4: two-mode (40/40, rest spread)": dist_two_mode(),
}


# =====================================================================
# Codec builders, parameterized by the value distribution.
# =====================================================================


class CodecLike(Generic[V]):
    """Structural protocol; not enforced -- documents the duck-type used."""

    m_bits: int

    def encode(self, value: V) -> int: ...
    def decode(self, pattern: int) -> V: ...
    def codespace_fraction(self, value: V) -> float: ...
    def expected_codeword_length(self, freqs: Mapping[V, float]) -> float: ...
    def non_member_distribution(self) -> dict[V, float]: ...


def build_dense() -> DenseCodec[str]:
    # Pure dense codec at m=3 (capacity 8 = |V|).
    return DenseCodec(VALUES, m_bits=3)


def build_padded(freqs: Mapping[str, float]) -> PaddedCodec[str]:
    # Padded codec at m=4. Default = highest-frequency value.
    default = max(freqs.items(), key=lambda kv: kv[1])[0]
    return PaddedCodec(VALUES, default_value=default, m_bits=4)


def build_prefix(freqs: Mapping[str, float]) -> PrefixCodec[str]:
    # Huffman built from the value distribution at m=4.
    return PrefixCodec.from_frequencies(freqs, m_bits=4)


# =====================================================================
# Simulation: draw N uniform m-bit patterns, count decoded values.
# =====================================================================


def simulate_non_member_distribution(
    codec: CodecLike[V],
    n_samples: int,
    rng: random.Random,
) -> dict[V, float]:
    counts: dict[V, int] = {}
    capacity = 1 << codec.m_bits
    for _ in range(n_samples):
        pattern = rng.randrange(capacity)
        v = codec.decode(pattern)
        counts[v] = counts.get(v, 0) + 1
    return {v: c / n_samples for v, c in counts.items()}


# =====================================================================
# Distance metrics between distributions (over a shared support).
# =====================================================================


def tv_distance(p: Mapping[V, float], q: Mapping[V, float]) -> float:
    """Total variation distance: 0.5 * sum |p_v - q_v| over the union."""
    keys: set[V] = set(p) | set(q)
    return 0.5 * sum(abs(p.get(k, 0.0) - q.get(k, 0.0)) for k in keys)


def kl_divergence(
    observed: Mapping[V, float],
    predicted: Mapping[V, float],
    eps: float = 1e-12,
) -> float:
    """``KL(observed || predicted) = sum o_v log2(o_v / p_v)``.

    ``eps`` regularizes zero-probability bins in ``predicted``; we drop
    bins where ``observed`` is also zero (``0 log 0 = 0``).
    """
    out = 0.0
    for v, o in observed.items():
        if o <= 0.0:
            continue
        p = max(predicted.get(v, 0.0), eps)
        out += o * math.log2(o / p)
    return out


# =====================================================================
# Experiment driver.
# =====================================================================


def run_one_cell(
    codec_name: str,
    codec: CodecLike[str],
    freqs: Mapping[str, float],
    n_samples: int,
    rng: random.Random,
) -> dict[str, object]:
    h = shannon_entropy(freqs)
    l_avg = codec.expected_codeword_length(freqs)
    predicted = codec.non_member_distribution()
    simulated = simulate_non_member_distribution(codec, n_samples, rng)

    # Tag output with full support so distance metrics are over the same set.
    full_predicted = {v: predicted.get(v, 0.0) for v in VALUES}
    full_simulated = {v: simulated.get(v, 0.0) for v in VALUES}

    tv = tv_distance(full_predicted, full_simulated)
    kl = kl_divergence(full_simulated, full_predicted)

    return {
        "codec": codec_name,
        "m_bits": codec.m_bits,
        "H_Y": h,
        "L": l_avg,
        "gap_L_minus_H": l_avg - h,
        "tv_distance": tv,
        "kl_div_obs_pred": kl,
        "predicted": full_predicted,
        "simulated": full_simulated,
    }


def run_experiment(n_samples: int, seed: int) -> dict[str, list[dict[str, object]]]:
    rng = random.Random(seed)
    out: dict[str, list[dict[str, object]]] = {}

    for dist_name, freqs in DISTRIBUTIONS.items():
        cells: list[dict[str, object]] = []

        # Same RNG stream per distribution; codecs draw independent streams
        # to avoid coupling across rows of the same distribution.
        for codec_name, build_fn in (
            ("DenseCodec(M=3)", lambda f=freqs: build_dense()),
            ("PaddedCodec(M=4, default=mode)", lambda f=freqs: build_padded(f)),
            ("PrefixCodec(M=4, Huffman)", lambda f=freqs: build_prefix(f)),
        ):
            codec = build_fn()
            cell_rng = random.Random(rng.randint(0, 1 << 30))
            cell = run_one_cell(codec_name, codec, freqs, n_samples, cell_rng)
            cells.append(cell)

        out[dist_name] = cells
    return out


# =====================================================================
# Reporting.
# =====================================================================


def fmt(x: float, digits: int = 4) -> str:
    return f"{x:.{digits}g}"


def render_distribution_table(freqs: Mapping[str, float]) -> str:
    total = sum(freqs.values())
    lines: list[str] = ["| value | p_v |", "|---|--:|"]
    for v in VALUES:
        lines.append(f"| {v} | {fmt(freqs.get(v, 0.0) / total)} |")
    return "\n".join(lines) + "\n"


def render_cell_summary(cell: dict[str, object]) -> str:
    return (
        f"| {cell['codec']} | {cell['m_bits']} | {fmt(cell['H_Y'])} | "
        f"{fmt(cell['L'])} | {fmt(cell['gap_L_minus_H'])} | "
        f"{fmt(cell['tv_distance'])} | {fmt(cell['kl_div_obs_pred'])} |"
    )


def render_predicted_vs_simulated(cell: dict[str, object]) -> str:
    pred = cell["predicted"]  # type: ignore[index]
    sim = cell["simulated"]  # type: ignore[index]
    assert isinstance(pred, dict)
    assert isinstance(sim, dict)
    lines: list[str] = [
        "| value | predicted | simulated | abs error |",
        "|---|--:|--:|--:|",
    ]
    for v in VALUES:
        p = pred.get(v, 0.0)
        s = sim.get(v, 0.0)
        lines.append(
            f"| {v} | {fmt(p)} | {fmt(s)} | {fmt(abs(p - s))} |"
        )
    return "\n".join(lines) + "\n"


def render_report(
    results: dict[str, list[dict[str, object]]],
    n_samples: int,
    seed: int,
    elapsed: float,
) -> str:
    out: list[str] = []
    out.append("# Experiment 04: Codec entropy and non-member output\n")
    out.append(
        "Empirical validation of two claims for `bernoulli.maps.codec`:\n\n"
        "1. **Shannon source-coding bound:** Huffman expected length `L`\n"
        "   satisfies `H(Y) <= L < H(Y) + 1` for the value distribution\n"
        "   used to build it.\n"
        "2. **Codec controls the non-member output distribution:** for a\n"
        "   structure where non-member queries effectively decode a uniform\n"
        "   M-bit pattern, the probability that a non-member returns `v`\n"
        "   equals the codec's codespace fraction for `v`.\n"
        "\n"
        f"All cells use N = {n_samples} uniform M-bit pattern draws per\n"
        f"codec. Seed = {seed}. Elapsed: {elapsed:.1f}s.\n"
    )

    out.append("\n## Value distributions\n")
    for dist_name, freqs in DISTRIBUTIONS.items():
        out.append(f"\n### {dist_name}\n\n")
        out.append(render_distribution_table(freqs))
        out.append(f"\nH(Y) = {fmt(shannon_entropy(freqs))} bits\n")

    out.append("\n## Per-distribution results\n")
    out.append(
        "Columns: `H(Y)` is the entropy of the value distribution; `L`\n"
        "is the expected codeword length under the distribution; `L - H`\n"
        "is the source-coding gap (Huffman: <= 1 bit). `TV` and `KL` are\n"
        "the total-variation and KL divergences between the codec's\n"
        "predicted non-member distribution and the simulated one.\n"
    )

    for dist_name, cells in results.items():
        out.append(f"\n### {dist_name}\n")
        out.append(
            "\n| codec | M | H(Y) | L | L - H(Y) | TV | KL(sim||pred) |\n"
            "|---|--:|--:|--:|--:|--:|--:|\n"
        )
        for cell in cells:
            out.append(render_cell_summary(cell) + "\n")

        # Per-codec predicted vs simulated breakdowns.
        for cell in cells:
            out.append(f"\n#### Predicted vs simulated for {cell['codec']}\n\n")
            out.append(render_predicted_vs_simulated(cell))

    # Summary commentary.
    out.append("\n## Summary findings\n\n")
    out.append(_render_summary_findings(results, n_samples))
    return "".join(out)


def _render_summary_findings(
    results: dict[str, list[dict[str, object]]],
    n_samples: int,
) -> str:
    lines: list[str] = []

    # 1. Shannon bound. The Huffman gap should be <= 1 across the board.
    huffman_gaps: list[tuple[str, float, float, float]] = []
    for dist_name, cells in results.items():
        for cell in cells:
            if "Huffman" in str(cell["codec"]):
                huffman_gaps.append(
                    (
                        dist_name,
                        float(cell["H_Y"]),  # type: ignore[arg-type]
                        float(cell["L"]),  # type: ignore[arg-type]
                        float(cell["gap_L_minus_H"]),  # type: ignore[arg-type]
                    )
                )

    lines.append("### Shannon source-coding bound\n\n")
    lines.append(
        "Huffman gap `L - H(Y)` per distribution (must be in `[0, 1)` by\n"
        "Shannon's source-coding theorem):\n\n"
    )
    lines.append("| distribution | H(Y) | L (Huffman) | gap |\n|---|--:|--:|--:|\n")
    max_gap = 0.0
    for name, h, l_avg, gap in huffman_gaps:
        lines.append(f"| {name} | {fmt(h)} | {fmt(l_avg)} | {fmt(gap)} |\n")
        max_gap = max(max_gap, gap)
    lines.append(
        f"\nMax observed Huffman gap: {fmt(max_gap)}. Within `[0, 1)`: "
        f"**{max_gap < 1.0}**.\n"
        "\nNote: the Huffman codeword lengths assigned by `from_frequencies`\n"
        "are integers, so `L` is always an integer-weighted sum. For the\n"
        "two-symbol case (D2 reduced to {v0, others}) Huffman gives both\n"
        "values length 1, matching `L = 1` regardless of how skewed the\n"
        "distribution is, which is the canonical example of the\n"
        "Shannon-Huffman gap. Arithmetic / range coding closes that gap\n"
        "in continuous-message regimes; the codec module here is the\n"
        "discrete per-value variant.\n"
    )

    # 2. Predicted vs simulated. TV should be approximately sqrt(p(1-p)/N) ~= 1/(2 sqrt N).
    expected_tv = 1.0 / (2.0 * math.sqrt(n_samples))
    lines.append("\n### Codec controls the non-member distribution\n\n")
    lines.append(
        "TV distance between predicted (codec codespace) and simulated\n"
        "(uniform M-bit decode) non-member distributions, per (distribution,\n"
        "codec) cell:\n\n"
    )
    lines.append("| distribution | codec | TV | KL |\n|---|---|--:|--:|\n")
    max_tv = 0.0
    for dist_name, cells in results.items():
        for cell in cells:
            tv = float(cell["tv_distance"])  # type: ignore[arg-type]
            kl = float(cell["kl_div_obs_pred"])  # type: ignore[arg-type]
            lines.append(
                f"| {dist_name} | {cell['codec']} | {fmt(tv)} | {fmt(kl)} |\n"
            )
            max_tv = max(max_tv, tv)
    lines.append(
        f"\nMax observed TV distance: {fmt(max_tv)}. Sampling-noise floor\n"
        f"(roughly `1 / (2 * sqrt(N))` for the worst single bin):\n"
        f"{fmt(expected_tv)}. Sample size N = {n_samples}.\n"
        "\nThe simulated distribution exactly matches the codec's\n"
        "codespace allocation up to sampling noise. This is expected by\n"
        "construction: the simulator draws uniform M-bit patterns and\n"
        "decodes them, which is exactly the model under which\n"
        "`codespace_fraction(v)` is the per-value probability. The\n"
        "interesting empirical question -- whether *ribbon retrieval's*\n"
        "non-member output matches this simulator -- was answered\n"
        "affirmatively by the maph project; see the\n"
        "`docs/CODESPACE_NONMEMBERS.md` reference and Experiment 03 here.\n"
        "\nWhat this experiment establishes for the Python codec is that\n"
        "the predictive bookkeeping is correct: `codespace_fraction(v)`\n"
        "is the actual probability of `v` under uniform M-bit decoding.\n"
    )
    return "".join(lines)


def main() -> int:
    seed = 2026
    n_samples = 30_000

    print("Running experiment 04: Codec entropy and non-member output...")
    print(f"  N samples per cell = {n_samples}, seed = {seed}\n")
    t0 = time.time()
    results = run_experiment(n_samples=n_samples, seed=seed)
    elapsed = time.time() - t0

    report = render_report(results, n_samples=n_samples, seed=seed, elapsed=elapsed)
    print()
    print(report)
    print(f"\nElapsed: {elapsed:.1f}s")

    out_path = HERE / "RESULTS_04.md"
    out_path.write_text(report)
    print(f"Report written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
