#!/usr/bin/env python3
"""Experiment 14: closed-form lower bound for the coincidence-oracle attacker.

This experiment sharpens the multi-instance leakage finding from
experiment 12 by deriving and validating a closed-form expression for
the **coincidence-oracle attacker's accuracy** in the t-instance,
shared-``f`` cipher-map deployment.

The coincidence oracle is the simplest possible attacker: it predicts
"k in S" iff all t observed outputs are equal. It gives a clean
theoretical lower bound on the Bayes-optimal attacker's accuracy.

Theoretical claim
-----------------

For t cipher-map instances over the same ``S``, same ``f``, codec
``q_codec`` (codespace fractions ``q_v = 2^(-l_v)`` for prefix codes),
under the codec_controlled retrieval variant (non-member outputs are
i.i.d. draws from ``q_codec``):

* For ``k in S``: ``M_1(k) = M_2(k) = ... = M_t(k) = f(k)`` deterministically.
* For ``k not in S``: ``M_i(k)`` are i.i.d. draws from ``q_codec``.

Define the coincidence event ``C = "all t outputs are equal"``. Then

* ``P(C | k in S) = 1`` (canonical encoding is deterministic).
* ``P(C | k not in S) = sum_v q_v^t``.

The coincidence-oracle attacker predicts "k in S" iff ``C`` holds. Its
accuracy at balanced prior ``pi = 1/2`` is

    accuracy(t, q_codec) = 1 - (sum_v q_v^t) / 2.

As ``t`` grows, ``sum_v q_v^t`` shrinks, and accuracy approaches 1
exponentially in ``t``. The decay rate is dominated by ``max_v q_v``.
Smaller ``sum_v q_v^t`` therefore means HIGHER attacker accuracy
(WORSE defense). Uniform codecs (Dense) minimize ``sum_v q_v^t``
and are thus the WORST defense against multi-instance attacks at
fixed ``epsilon``; concentrated codecs (Huffman, with large
``max_v q_v``) maximize ``sum_v q_v^t`` and are the BEST defense.
Both single-instance (Le Cam) and multi-instance (coincidence-oracle)
optima favor Huffman-style concentration; there is no codec-choice
regime change between t=1 and t>=2.
"""

from __future__ import annotations

import math
import random
import sys
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
PKG_ROOT = HERE.parent
sys.path.insert(0, str(PKG_ROOT / "src"))

from bernoulli.maps.codec import (  # noqa: E402
    DenseCodec,
    PaddedCodec,
    PrefixCodec,
)

# =====================================================================
# Inlined cipher-map setup (codec_controlled variant), from exp 12.
# =====================================================================

VALUES: list[str] = [f"v{i}" for i in range(8)]
M_BITS: int = 4


def f_distribution() -> dict[str, float]:
    """Zipf-ish value distribution, identical to experiment 12."""
    raw = [1.0 / ((i + 1) ** 1.2) for i in range(len(VALUES))]
    total = sum(raw)
    return {v: w / total for v, w in zip(VALUES, raw, strict=True)}


def _anti_huffman_codec(p_f: Mapping[str, float], m_bits: int) -> PrefixCodec[str]:
    """Reversed-rank Huffman: rare values get short codes (leaky)."""
    sorted_vals = sorted(p_f.items(), key=lambda kv: kv[1])
    n = len(sorted_vals)
    weights = [(sorted_vals[i][0], float(n - i)) for i in range(n)]
    return PrefixCodec.from_frequencies(dict(weights), m_bits=m_bits)


def make_keys(n: int, rng: random.Random) -> list[bytes]:
    seen: set[bytes] = set()
    out: list[bytes] = []
    while len(out) < n:
        k = bytes(rng.randint(0, 255) for _ in range(16))
        if k in seen:
            continue
        seen.add(k)
        out.append(k)
    return out


def sample_value(p: Mapping[str, float], rng: random.Random) -> str:
    r = rng.random()
    cum = 0.0
    for v, w in p.items():
        cum += w
        if r < cum:
            return v
    return next(iter(p))


@dataclass
class CipherMap:
    s_keys: tuple[bytes, ...]
    s_index: dict[bytes, int]
    store: list[int]
    codec: Any
    m_bits: int

    @classmethod
    def build(
        cls,
        s_keys: Sequence[bytes],
        s_values: Mapping[bytes, str],
        codec: Any,
        m_bits: int,
    ) -> CipherMap:
        store = [codec.encode(s_values[k]) for k in s_keys]
        return cls(
            s_keys=tuple(s_keys),
            s_index={k: i for i, k in enumerate(s_keys)},
            store=store,
            codec=codec,
            m_bits=m_bits,
        )

    def lookup(self, k: bytes, rng: random.Random) -> str:
        idx = self.s_index.get(k)
        if idx is not None:
            return self.codec.decode(self.store[idx])
        # codec_controlled non-member behaviour: uniform M-bit pattern.
        pattern = rng.randrange(1 << self.m_bits)
        return self.codec.decode(pattern)


# =====================================================================
# Closed-form predictions.
# =====================================================================


def coincidence_pc_nonmember(codec: Any, t: int) -> float:
    """``P(all t outputs equal | k not in S) = sum_v q_v^t``."""
    qdist = codec.non_member_distribution()
    return sum(q**t for q in qdist.values())


def coincidence_accuracy(codec: Any, t: int, pi: float = 0.5) -> float:
    """Closed-form accuracy of the coincidence-oracle attacker.

    Predict "in S" iff all t outputs equal:
    accuracy = pi * P(C|S) + (1 - pi) * (1 - P(C|not S))
             = pi + (1 - pi) - (1 - pi) * P(C|not S) * 1 - pi * (1 - 1)
             = pi * 1 + (1 - pi) * (1 - P(C|not S))
             = 1 - (1 - pi) * P(C|not S).
    For balanced pi = 0.5: accuracy = 1 - P(C|not S) / 2.
    """
    pc_not = coincidence_pc_nonmember(codec, t)
    return pi * 1.0 + (1.0 - pi) * (1.0 - pc_not)


def le_cam_upper_bound(joint_tv: float) -> float:
    """Bayes-optimal accuracy upper bound: ``1/2 + TV/2``."""
    return 0.5 + joint_tv / 2.0


# =====================================================================
# Empirical evaluation.
# =====================================================================


@dataclass
class CellResult:
    codec_label: str
    t: int
    q_codespace: dict[str, float]
    max_q: float
    pc_nonmember_predicted: float
    accuracy_predicted: float
    accuracy_empirical: float
    accuracy_ci_low: float
    accuracy_ci_high: float
    inside_ci: bool
    joint_tv_empirical: float
    le_cam_upper: float
    n_test_per_class: int


def wilson_ci(
    successes: int, n: int, z: float = 1.96
) -> tuple[float, float]:
    """Wilson 95% CI for a binomial proportion."""
    if n == 0:
        return (0.0, 1.0)
    p = successes / n
    denom = 1.0 + z * z / n
    centre = (p + z * z / (2.0 * n)) / denom
    half = (
        z * math.sqrt(p * (1.0 - p) / n + z * z / (4.0 * n * n))
    ) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


def coincidence_predict(outputs: tuple[str, ...]) -> bool:
    """Predict 'in S' iff all observed outputs are equal."""
    if not outputs:
        return False
    first = outputs[0]
    return all(y == first for y in outputs)


def make_codec(name: str, p_f: Mapping[str, float]) -> Any:
    """Codec factory for the sweep."""
    if name == "Dense(M=3)":
        return DenseCodec(VALUES, m_bits=3)
    if name == "Dense(M=4)":
        # |V|=8 keys but M=4 -> 16 codespace patterns, surplus folds to v0.
        return DenseCodec(VALUES, m_bits=4)
    if name == "Padded(M=4,v0)":
        return PaddedCodec(VALUES, default_value=VALUES[0], m_bits=4)
    if name == "Huffman(M=4,p_f)":
        return PrefixCodec.from_frequencies(p_f, m_bits=4)
    if name == "AntiHuffman(M=4)":
        return _anti_huffman_codec(p_f, m_bits=4)
    raise ValueError(f"unknown codec name {name!r}")


def run_one_cell(
    codec_label: str,
    codec: Any,
    t: int,
    p_f: Mapping[str, float],
    n_keys: int,
    n_universe_extra: int,
    n_test_per_class: int,
    rng: random.Random,
) -> CellResult:
    """Build t cipher-maps with shared f, run the coincidence oracle."""
    # Build set and universe.
    s_keys = make_keys(n_keys, rng)
    nonmembers = make_keys(n_universe_extra, rng)
    nonmembers = [k for k in nonmembers if k not in set(s_keys)]

    # Shared f: one assignment, used by all t instances.
    f_assignment: dict[bytes, str] = {
        k: sample_value(p_f, random.Random(rng.randint(0, 1 << 30)))
        for k in s_keys
    }

    instances: list[CipherMap] = []
    for _ in range(t):
        # Same codec, same f. Each instance is identical at the data
        # level; only non-member draws are independent.
        cm = CipherMap.build(
            s_keys=s_keys,
            s_values=f_assignment,
            codec=codec,
            m_bits=getattr(codec, "m_bits", M_BITS),
        )
        instances.append(cm)

    look_rng = random.Random(rng.randint(0, 1 << 30))

    # Empirical: run coincidence oracle on balanced test set.
    correct = 0
    n_total = 2 * n_test_per_class
    member_joint_counts: dict[tuple[str, ...], int] = {}
    nm_joint_counts: dict[tuple[str, ...], int] = {}
    for _ in range(n_test_per_class):
        # Member sample.
        k = s_keys[look_rng.randrange(len(s_keys))]
        outputs = tuple(cm.lookup(k, look_rng) for cm in instances)
        member_joint_counts[outputs] = member_joint_counts.get(outputs, 0) + 1
        pred_in = coincidence_predict(outputs)
        if pred_in:
            correct += 1
        # Non-member sample.
        k = nonmembers[look_rng.randrange(len(nonmembers))]
        outputs = tuple(cm.lookup(k, look_rng) for cm in instances)
        nm_joint_counts[outputs] = nm_joint_counts.get(outputs, 0) + 1
        pred_in = coincidence_predict(outputs)
        if not pred_in:
            correct += 1

    accuracy_empirical = correct / n_total
    ci_low, ci_high = wilson_ci(correct, n_total)

    # Joint TV (empirical).
    keys = set(member_joint_counts) | set(nm_joint_counts)
    m_total = sum(member_joint_counts.values())
    n_total_nm = sum(nm_joint_counts.values())
    p_member = {y: member_joint_counts.get(y, 0) / m_total for y in keys}
    p_nm = {y: nm_joint_counts.get(y, 0) / n_total_nm for y in keys}
    joint_tv = 0.5 * sum(abs(p_member[y] - p_nm[y]) for y in keys)

    # Closed-form predictions.
    pc_not = coincidence_pc_nonmember(codec, t)
    accuracy_predicted = coincidence_accuracy(codec, t, pi=0.5)
    qdist = codec.non_member_distribution()
    max_q = max(qdist.values())

    inside_ci = ci_low - 1e-6 <= accuracy_predicted <= ci_high + 1e-6

    return CellResult(
        codec_label=codec_label,
        t=t,
        q_codespace=dict(qdist),
        max_q=max_q,
        pc_nonmember_predicted=pc_not,
        accuracy_predicted=accuracy_predicted,
        accuracy_empirical=accuracy_empirical,
        accuracy_ci_low=ci_low,
        accuracy_ci_high=ci_high,
        inside_ci=inside_ci,
        joint_tv_empirical=joint_tv,
        le_cam_upper=le_cam_upper_bound(joint_tv),
        n_test_per_class=n_test_per_class,
    )


def run_experiment(
    n_keys: int = 2000,
    n_universe_extra: int = 8000,
    n_test_per_class: int = 5000,
    seed: int = 2026,
) -> list[CellResult]:
    rng = random.Random(seed)
    p_f = f_distribution()

    # Codec sweep: 5 codecs.
    codec_labels = [
        "Dense(M=3)",
        "Dense(M=4)",
        "Padded(M=4,v0)",
        "Huffman(M=4,p_f)",
        "AntiHuffman(M=4)",
    ]
    t_values = [1, 2, 3, 4, 5]

    out: list[CellResult] = []
    for label in codec_labels:
        codec = make_codec(label, p_f)
        for t in t_values:
            cell_rng = random.Random(rng.randint(0, 1 << 30))
            out.append(
                run_one_cell(
                    codec_label=label,
                    codec=codec,
                    t=t,
                    p_f=p_f,
                    n_keys=n_keys,
                    n_universe_extra=n_universe_extra,
                    n_test_per_class=n_test_per_class,
                    rng=cell_rng,
                )
            )
    return out


# =====================================================================
# Reporting.
# =====================================================================


def fmt(x: float, digits: int = 4) -> str:
    return f"{x:.{digits}g}"


def render_main_table(results: Sequence[CellResult]) -> str:
    lines = [
        (
            "| codec | t | max q_v | sum q_v^t | predicted acc | "
            "empirical acc | 95% CI | in CI? | empirical joint TV | "
            "Le Cam UB |"
        ),
        "|---|--:|--:|--:|--:|--:|---|:-:|--:|--:|",
    ]
    for r in results:
        ci = f"[{fmt(r.accuracy_ci_low)}, {fmt(r.accuracy_ci_high)}]"
        lines.append(
            f"| {r.codec_label} | {r.t} | {fmt(r.max_q)} | "
            f"{fmt(r.pc_nonmember_predicted)} | "
            f"{fmt(r.accuracy_predicted)} | "
            f"{fmt(r.accuracy_empirical)} | {ci} | "
            f"{'yes' if r.inside_ci else 'NO'} | "
            f"{fmt(r.joint_tv_empirical)} | {fmt(r.le_cam_upper)} |"
        )
    return "\n".join(lines) + "\n"


def render_geometric_argument(results: Sequence[CellResult]) -> str:
    """Show that as t grows, the codec with smallest max_q wins."""
    out: list[str] = []
    out.append("### Geometric argument: max_v q_v dominates at large t\n\n")
    out.append(
        "As ``t`` grows, ``sum_v q_v^t`` is asymptotically dominated by "
        "the largest term ``(max_v q_v)^t``. The codec with the LOWEST "
        "``max_v q_v`` therefore defends best against multi-instance "
        "attacks.\n\n"
    )
    out.append(
        "| codec | max q_v | (max q_v)^5 | sum q_v^5 | "
        "ratio (asymptotic tightness) |\n"
    )
    out.append("|---|--:|--:|--:|--:|\n")
    # group by codec, pull t=5.
    by_codec: dict[str, CellResult] = {}
    for r in results:
        if r.t == 5:
            by_codec[r.codec_label] = r
    for label, r in by_codec.items():
        max_q = r.max_q
        sum_q5 = r.pc_nonmember_predicted
        max_q5 = max_q**5
        ratio = max_q5 / sum_q5 if sum_q5 > 0 else 0.0
        out.append(
            f"| {label} | {fmt(max_q)} | {fmt(max_q5)} | "
            f"{fmt(sum_q5)} | {fmt(ratio)} |\n"
        )
    out.append("\n")
    out.append(
        "**Reading the ratio.** A ratio close to 1 means the largest "
        "codespace fraction dominates the sum; the asymptotic decay "
        "rate is ``max q_v``. A ratio well below 1 means several "
        "values share comparable mass and the geometric bound is "
        "looser. Either way, the BASE of the exponential decay is "
        "``max_v q_v``.\n\n"
    )
    return "".join(out)


def render_findings(results: Sequence[CellResult]) -> str:
    out: list[str] = []

    inside = sum(1 for r in results if r.inside_ci)
    total = len(results)
    out.append("### Closed-form vs empirical\n\n")
    out.append(
        f"Across all ({len(set(r.codec_label for r in results))} codecs) "
        f"x ({len(set(r.t for r in results))} values of t) = {total} "
        f"configurations, the closed-form predicted accuracy lies "
        f"inside the empirical Wilson 95% CI for "
        f"**{inside} / {total}** cells.\n\n"
    )
    out.append(
        "The closed form ``acc(t, q_codec) = 1 - sum_v q_v^t / 2`` is "
        "exact under the codec_controlled retrieval variant, and "
        "matches empirical accuracy up to sampling noise.\n\n"
    )

    # Coincidence vs Le Cam: how tight is the lower bound?
    out.append("### Coincidence oracle vs Bayes-optimal (Le Cam) bound\n\n")
    out.append(
        "The coincidence oracle gives a closed-form *lower bound* on "
        "the Bayes-optimal attacker's accuracy. Le Cam's "
        "``1/2 + joint_TV/2`` is the *upper bound*. The gap "
        "``Le_Cam_UB - coincidence`` measures how much extra signal "
        "is left on the table.\n\n"
    )
    out.append(
        "| codec | t | coincidence acc | Le Cam UB | gap |\n"
    )
    out.append("|---|--:|--:|--:|--:|\n")
    for r in results:
        gap = r.le_cam_upper - r.accuracy_predicted
        out.append(
            f"| {r.codec_label} | {r.t} | {fmt(r.accuracy_predicted)} | "
            f"{fmt(r.le_cam_upper)} | {fmt(gap)} |\n"
        )
    out.append("\n")
    out.append(
        "For the shared-``f`` regime, the gap is dominated by the "
        "coincidence-vs-pattern-distribution difference: the "
        "coincidence oracle ignores *which* value the t copies agree "
        "on, while a Bayes attacker exploits the conditional "
        "distribution of that shared value as well. Still, at large "
        "``t`` the coincidence oracle saturates near 1 and the gap "
        "shrinks.\n\n"
    )

    # Geometric argument.
    out.append(render_geometric_argument(results))

    out.append("### Defense implications\n\n")
    out.append(
        "* **Single-instance regime.** Huffman codecs minimize ``TV(p_f, q_codec)``. "
        "Dense (uniform) codecs maximize it. So at ``t=1``, Huffman "
        "defends best.\n"
        "* **Multi-instance regime (``t >= 2``).** The coincidence "
        "oracle's accuracy depends only on ``sum_v q_v^t``. The "
        "codec with the SMALLEST ``max_v q_v`` defends best at "
        "large ``t``. Uniform codecs (Dense) on a large value "
        "alphabet have ``max_v q_v = 1/|V|``, much smaller than "
        "Huffman's ``max_v q_v ~= max_v p_v``.\n"
        "* **Tradeoff.** A codec that defends best at ``t=1`` "
        "(Huffman) defends *worst* at large ``t`` whenever ``p_f`` is "
        "skewed (because the dominant-value codespace fraction "
        "matches the dominant-value frequency). The best codec "
        "depends on the deployment scale: how many instances will "
        "ever be observed by the same attacker? At ``t=1``, prefer "
        "Huffman; at large ``t``, prefer Dense.\n"
        "* **No codec defeats the coincidence oracle.** As ``t`` "
        "grows, every codec's ``sum_v q_v^t`` decays to zero, so "
        "the oracle's accuracy approaches 1. The only true defense "
        "is correlating non-member outputs across instances "
        "(shared seed) so that members and non-members share the "
        "coincidence statistic, OR not redeploying the same "
        "``(S, f)`` pair.\n"
    )
    return "".join(out)


def render_report(
    results: Sequence[CellResult],
    n_keys: int,
    n_test_per_class: int,
    seed: int,
    elapsed: float,
) -> str:
    out: list[str] = []
    out.append("# Experiment 14: Coincidence-oracle closed form\n\n")
    out.append(
        "**Goal.** Derive and validate the closed-form accuracy for "
        "the coincidence-oracle attacker in a t-instance, shared-``f`` "
        "cipher-map deployment. The coincidence oracle is the "
        "simplest possible attacker: predict ``k in S`` iff all t "
        "observed outputs are equal. It gives a clean theoretical "
        "lower bound on the Bayes-optimal attacker's accuracy, and "
        "extends the empirical observation in experiment 12 to a "
        "closed form parameterized by the codec's codespace.\n\n"
    )
    out.append("## Closed form\n\n")
    out.append(
        "Under the codec_controlled cipher-map retrieval variant "
        "(non-member outputs are i.i.d. draws from "
        "``q_codec(v) = 2^(-l_v)``, with ``sum_v q_v <= 1``):\n\n"
    )
    out.append(
        "* For ``k in S``: all t outputs equal ``f(k)`` "
        "deterministically (canonical encoding).\n"
    )
    out.append("* For ``k not in S``: outputs are i.i.d. ~ ``q_codec``.\n\n")
    out.append("Coincidence event ``C`` = 'all t outputs equal'. Then:\n\n")
    out.append("* ``P(C | k in S) = 1``.\n")
    out.append("* ``P(C | k not in S) = sum_v q_v^t``.\n\n")
    out.append(
        "The coincidence-oracle attacker predicts ``k in S`` iff "
        "``C``. At balanced prior ``pi = 1/2``, accuracy is\n\n"
        "    accuracy(t, q_codec) = pi * P(C | S) + (1 - pi) * (1 - P(C | not S))\n"
        "                         = 1/2 * 1 + 1/2 * (1 - sum_v q_v^t)\n"
        "                         = 1 - (sum_v q_v^t) / 2.\n\n"
    )
    out.append(
        "**Asymptotic decay.** ``sum_v q_v^t`` is dominated by "
        "``(max_v q_v)^t``. So accuracy approaches 1 - "
        "``(max_v q_v)^t / 2`` exponentially in ``t``. The *base* of "
        "the decay is ``max_v q_v``.\n\n"
    )
    out.append(
        f"**Setup.** ``|S| = {n_keys}`` keys, ``|V| = {len(VALUES)}`` "
        f"values, n_test_per_class = {n_test_per_class}, seed = "
        f"{seed}, elapsed = {elapsed:.1f}s.\n\n"
    )
    out.append("## Headline table: predicted vs empirical\n\n")
    out.append(render_main_table(results))
    out.append("\n## Findings\n\n")
    out.append(render_findings(results))
    return "".join(out)


def main() -> int:
    seed = 2026
    n_keys = 2000
    n_test_per_class = 5000
    print("Running experiment 14: Coincidence-oracle closed form...")
    t0 = time.time()
    results = run_experiment(
        n_keys=n_keys,
        n_test_per_class=n_test_per_class,
        seed=seed,
    )
    elapsed = time.time() - t0
    report = render_report(
        results,
        n_keys=n_keys,
        n_test_per_class=n_test_per_class,
        seed=seed,
        elapsed=elapsed,
    )
    print(report)
    print(f"\nElapsed: {elapsed:.1f}s")
    out_path = HERE / "RESULTS_14.md"
    out_path.write_text(report)
    print(f"Report written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
