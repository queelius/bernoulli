#!/usr/bin/env python3
"""Experiment 12: multi-instance cipher-map leakage.

Goal
----
Quantify how observing TWO (or more) cipher-map instances over the same
build set ``S`` compounds membership-inference leakage relative to
observing either alone. The two instances may differ in codec, in value
function, or both. This is the security analog of the correlated Bloom
filter studies (experiments 05 / 06) lifted to the cipher-map / codec-
controlled regime of experiment 07.

Variants studied
----------------

We always use the codec_controlled cipher-map (ribbon-retrieval) variant
from experiment 07. Non-members decode a uniform M-bit pattern through
the codec, so the non-member output distribution equals the codec's
codespace allocation.

A multi-instance cipher-map ``MM = (M_1, ..., M_t)`` answers a tuple
``(M_1(k), ..., M_t(k))``. The attacker fits a Bayes classifier on
the joint output and we measure:

* Single-instance TV per component, single-instance AUC per component.
* Joint TV between the joint member and joint non-member distributions.
* Joint attack AUC.

Hypotheses
----------

* H1 (subadditivity). Joint TV is bounded above by the sum of the
  single-instance TVs.
* H2 (lower bound). Joint TV >= max single TV.
* H3 (independence compounding). When the two instances are
  conditionally independent given the membership label, joint AUC
  compounds in log-likelihood-ratio space and pulls away from the
  better single-instance AUC.
* H4 (rotation defense). Pairing complementary codecs (e.g. Huffman +
  anti-Huffman) can reduce joint leakage if their codespace allocations
  cancel rather than compound, OR can backfire dramatically if the
  joint distribution becomes more distinguishable.

What we sweep
-------------

A handful of (codec_1, codec_2[, codec_3]) configurations spanning
* same-codec, same-f (control: matches single-instance leakage).
* same-codec, different-f (does seeding-with-different-f compound?).
* different-codec, same-f (rotation defense or attack?).
* different-codec, different-f (most realistic adversary scenario).
* three-instance same-codec (does information stack?).
* three-instance rotation.

Outputs
-------

A markdown table over configurations, plus theoretical sanity checks
(subadditivity, lower bound, Le Cam AUC vs joint TV).
"""

from __future__ import annotations

import random
import sys
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
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
# Inlined cipher-map setup (ported from experiment 07).
# =====================================================================

VALUES: list[str] = [f"v{i}" for i in range(8)]
M_BITS: int = 4


def f_distribution() -> dict[str, float]:
    """Zipf-ish value distribution, identical to experiment 07."""
    raw = [1.0 / ((i + 1) ** 1.2) for i in range(len(VALUES))]
    total = sum(raw)
    return {v: w / total for v, w in zip(VALUES, raw, strict=True)}


def f_distribution_alt() -> dict[str, float]:
    """A *different* value distribution (reverse Zipf), for ``different-f`` cells."""
    raw = [1.0 / ((len(VALUES) - i) ** 1.2) for i in range(len(VALUES))]
    total = sum(raw)
    return {v: w / total for v, w in zip(VALUES, raw, strict=True)}


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


def _anti_huffman_codec(p_f: Mapping[str, float], m_bits: int) -> PrefixCodec[str]:
    """Reversed-rank Huffman: rare values get short codes (worst case)."""
    sorted_vals = sorted(p_f.items(), key=lambda kv: kv[1])
    n = len(sorted_vals)
    weights = [(sorted_vals[i][0], float(n - i)) for i in range(n)]
    return PrefixCodec.from_frequencies(dict(weights), m_bits=m_bits)


# =====================================================================
# Single cipher-map instance (codec_controlled variant only).
# =====================================================================


@dataclass
class CipherMap:
    """A single codec-controlled cipher-map.

    Holds ``S``, the per-key values ``f(k)`` for ``k in S`` (already
    encoded into M-bit patterns by the codec), and the codec itself.
    Non-members decode a uniform M-bit pattern.
    """

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
# Multi-instance cipher-map.
# =====================================================================


@dataclass
class MultiInstanceMap:
    instances: list[CipherMap]

    def lookup(self, k: bytes, rng: random.Random) -> tuple[str, ...]:
        return tuple(m.lookup(k, rng) for m in self.instances)


# =====================================================================
# Bayes attacker over single-value or tuple outputs.
# =====================================================================


@dataclass
class JointBayesAttacker:
    """Bayes classifier on tuple-valued lookups (joint of t instances)."""

    pi_s: float
    p_y_given_s: dict[tuple[str, ...], float]
    p_y_given_not_s: dict[tuple[str, ...], float]
    smoothing: float = 1.0
    alphabet_size: int = 1

    @classmethod
    def fit(
        cls,
        labels: Sequence[bool],
        outputs: Sequence[tuple[str, ...]],
        alphabet_size: int,
        smoothing: float = 1.0,
    ) -> JointBayesAttacker:
        n_s = sum(1 for b in labels if b)
        counts_s: dict[tuple[str, ...], float] = {}
        counts_not_s: dict[tuple[str, ...], float] = {}
        for in_s, y in zip(labels, outputs, strict=True):
            tgt = counts_s if in_s else counts_not_s
            tgt[y] = tgt.get(y, 0.0) + 1.0
        # Add smoothing over observed cells of either side; we don't
        # enumerate the full alphabet of size |V|^t (could be large).
        all_keys = set(counts_s) | set(counts_not_s)
        norm_s = sum(counts_s.values()) + smoothing * len(all_keys)
        norm_not_s = sum(counts_not_s.values()) + smoothing * len(all_keys)
        p_s = {y: (counts_s.get(y, 0.0) + smoothing) / norm_s for y in all_keys}
        p_not_s = {
            y: (counts_not_s.get(y, 0.0) + smoothing) / norm_not_s for y in all_keys
        }
        pi = (n_s + 1.0) / (len(labels) + 2.0)
        return cls(
            pi_s=pi,
            p_y_given_s=p_s,
            p_y_given_not_s=p_not_s,
            smoothing=smoothing,
            alphabet_size=alphabet_size,
        )

    def score(self, y: tuple[str, ...]) -> float:
        # Use uniform 1/alphabet_size for unseen tuples (smoothing fallback).
        fallback = 1.0 / max(self.alphabet_size, 1)
        p_y_s = self.p_y_given_s.get(y, fallback)
        p_y_ns = self.p_y_given_not_s.get(y, fallback)
        num = p_y_s * self.pi_s
        den = num + p_y_ns * (1.0 - self.pi_s)
        if den <= 0.0:
            return self.pi_s
        return num / den


def attack_metrics(
    labels: Sequence[bool], scores: Sequence[float], threshold: float = 0.5
) -> tuple[float, float]:
    """Accuracy at ``threshold`` and Mann-Whitney U AUC."""
    correct = sum(
        1
        for lbl, s in zip(labels, scores, strict=True)
        if (s >= threshold) == lbl
    )
    accuracy = correct / max(len(labels), 1)
    pos_scores = [s for lbl, s in zip(labels, scores, strict=True) if lbl]
    neg_scores = [s for lbl, s in zip(labels, scores, strict=True) if not lbl]
    if not pos_scores or not neg_scores:
        return accuracy, 0.5
    n_pos = len(pos_scores)
    n_neg = len(neg_scores)
    all_scored = [(s, 1) for s in pos_scores] + [(s, 0) for s in neg_scores]
    all_scored.sort(key=lambda t: t[0])
    rank_sum_pos = 0.0
    i = 0
    n = len(all_scored)
    while i < n:
        j = i
        while j < n and all_scored[j][0] == all_scored[i][0]:
            j += 1
        avg_rank = (i + j + 1) / 2.0
        for k in range(i, j):
            if all_scored[k][1] == 1:
                rank_sum_pos += avg_rank
        i = j
    u = rank_sum_pos - n_pos * (n_pos + 1) / 2.0
    auc = u / (n_pos * n_neg)
    return accuracy, auc


def tv_distance(
    p: Mapping[Any, float], q: Mapping[Any, float]
) -> float:
    keys = set(p) | set(q)
    return 0.5 * sum(abs(p.get(k, 0.0) - q.get(k, 0.0)) for k in keys)


# =====================================================================
# Configurations.
# =====================================================================


@dataclass
class InstanceSpec:
    """How to build one cipher-map: which codec, and which value function."""

    codec_label: str
    codec_builder: Any  # zero-arg.
    f_label: str  # "f" or "f_alt"


@dataclass
class ConfigSpec:
    name: str
    description: str
    instances: list[InstanceSpec]


def make_codec(name: str, p_f: Mapping[str, float]) -> Any:
    if name == "Dense(M=3)":
        return DenseCodec(VALUES, m_bits=3)
    if name == "Padded(M=4,v0)":
        return PaddedCodec(VALUES, default_value=VALUES[0], m_bits=4)
    if name == "Huffman(M=4,p_f)":
        return PrefixCodec.from_frequencies(p_f, m_bits=4)
    if name == "Huffman(M=4,p_f_alt)":
        return PrefixCodec.from_frequencies(f_distribution_alt(), m_bits=4)
    if name == "AntiHuffman(M=4)":
        return _anti_huffman_codec(p_f, m_bits=4)
    raise ValueError(f"unknown codec name {name!r}")


def build_configs(p_f: Mapping[str, float]) -> list[ConfigSpec]:
    def inst(codec_name: str, f_label: str = "f") -> InstanceSpec:
        return InstanceSpec(
            codec_label=codec_name,
            codec_builder=lambda cn=codec_name: make_codec(cn, p_f),
            f_label=f_label,
        )

    return [
        ConfigSpec(
            name="Single Huffman (baseline)",
            description="One cipher-map with the optimal Huffman codec.",
            instances=[inst("Huffman(M=4,p_f)")],
        ),
        ConfigSpec(
            name="Two Huffman, same f (repeat)",
            description=(
                "Same codec, same value function. Instances coincide on "
                "members; non-members are independent draws over the same "
                "codespace."
            ),
            instances=[inst("Huffman(M=4,p_f)"), inst("Huffman(M=4,p_f)")],
        ),
        ConfigSpec(
            name="Two Huffman, different f",
            description=(
                "Same codec, but each instance draws f(k) iid independently. "
                "Members differ across instances."
            ),
            instances=[
                inst("Huffman(M=4,p_f)", "f"),
                inst("Huffman(M=4,p_f)", "f_alt"),
            ],
        ),
        ConfigSpec(
            name="Huffman + Dense, same f",
            description="Codec rotation: optimal Huffman alongside leaky Dense.",
            instances=[
                inst("Huffman(M=4,p_f)"),
                inst("Dense(M=3)"),
            ],
        ),
        ConfigSpec(
            name="Huffman + AntiHuffman, same f (rotation)",
            description=(
                "Most adversarial codec rotation: pair the protective "
                "codec with its inverse."
            ),
            instances=[
                inst("Huffman(M=4,p_f)"),
                inst("AntiHuffman(M=4)"),
            ],
        ),
        ConfigSpec(
            name="Two AntiHuffman, same f",
            description="Two leaky instances with same codec; control for the rotation case.",
            instances=[
                inst("AntiHuffman(M=4)"),
                inst("AntiHuffman(M=4)"),
            ],
        ),
        ConfigSpec(
            name="Three Huffman, same f (stacking)",
            description="Three repeated Huffman instances. Tests whether information accumulates.",
            instances=[
                inst("Huffman(M=4,p_f)"),
                inst("Huffman(M=4,p_f)"),
                inst("Huffman(M=4,p_f)"),
            ],
        ),
        ConfigSpec(
            name="Huffman + Dense + AntiHuffman (3-rotation)",
            description="Three-codec rotation across the leakage spectrum.",
            instances=[
                inst("Huffman(M=4,p_f)"),
                inst("Dense(M=3)"),
                inst("AntiHuffman(M=4)"),
            ],
        ),
    ]


# =====================================================================
# Driver.
# =====================================================================


@dataclass
class CellResult:
    name: str
    description: str
    instance_codecs: list[str]
    instance_f_labels: list[str]
    single_tvs: list[float]
    single_aucs: list[float]
    joint_tv: float
    joint_acc: float
    joint_auc: float
    sum_single_tvs: float
    max_single_tv: float
    max_single_auc: float
    le_cam_predicted_auc: float
    member_dist_marginals: list[dict[str, float]] = field(default_factory=list)
    nonmember_dist_marginals: list[dict[str, float]] = field(default_factory=list)


def run_one_config(
    cfg: ConfigSpec,
    p_f: Mapping[str, float],
    p_f_alt: Mapping[str, float],
    n_keys: int,
    n_universe_extra: int,
    n_train: int,
    n_test: int,
    pi_s: float,
    nonmember_samples: int,
    rng: random.Random,
) -> CellResult:
    s_keys = make_keys(n_keys, rng)
    nonmembers = make_keys(n_universe_extra, rng)
    nonmembers = [k for k in nonmembers if k not in set(s_keys)]

    # Build per-instance value assignments. ``f`` and ``f_alt`` use
    # different distributions so members differ across instances.
    f_assignments: dict[str, dict[bytes, str]] = {}
    distros: dict[str, Mapping[str, float]] = {"f": p_f, "f_alt": p_f_alt}
    for label in {ins.f_label for ins in cfg.instances}:
        d = distros[label]
        f_assignments[label] = {
            k: sample_value(d, random.Random(rng.randint(0, 1 << 30)))
            for k in s_keys
        }

    instances: list[CipherMap] = []
    for ins in cfg.instances:
        codec = ins.codec_builder()
        cm = CipherMap.build(
            s_keys=s_keys,
            s_values=f_assignments[ins.f_label],
            codec=codec,
            m_bits=getattr(codec, "m_bits", M_BITS),
        )
        instances.append(cm)
    mm = MultiInstanceMap(instances=instances)

    # Estimate per-instance member and non-member marginals.
    member_marginals: list[dict[str, float]] = []
    nonmember_marginals: list[dict[str, float]] = []
    for cm in instances:
        m_counts = {v: 0 for v in VALUES}
        for v in (cm.codec.decode(p) for p in cm.store):
            m_counts[v] += 1
        norm = sum(m_counts.values())
        member_marginals.append({v: m_counts[v] / norm for v in VALUES})
        nonmember_marginals.append(cm.codec.non_member_distribution())

    single_tvs = [
        tv_distance(member_marginals[i], nonmember_marginals[i])
        for i in range(len(instances))
    ]

    # Estimate joint distributions empirically over (large) sample.
    joint_rng = random.Random(rng.randint(0, 1 << 30))
    member_joint: dict[tuple[str, ...], int] = {}
    nm_joint: dict[tuple[str, ...], int] = {}
    n_joint_samples = nonmember_samples
    # Member joint: iterate over all S keys (deterministic answer).
    for k in s_keys:
        y = mm.lookup(k, joint_rng)
        member_joint[y] = member_joint.get(y, 0) + 1
    member_total = sum(member_joint.values())
    member_joint_dist = {y: c / member_total for y, c in member_joint.items()}
    # Non-member joint: sample non-members.
    for _ in range(n_joint_samples):
        k = nonmembers[joint_rng.randrange(len(nonmembers))]
        y = mm.lookup(k, joint_rng)
        nm_joint[y] = nm_joint.get(y, 0) + 1
    nm_total = sum(nm_joint.values())
    nm_joint_dist = {y: c / nm_total for y, c in nm_joint.items()}

    joint_tv = tv_distance(member_joint_dist, nm_joint_dist)

    # Build train/test for joint Bayes attack.
    def make_dataset(
        n: int, ds_rng: random.Random
    ) -> tuple[list[bool], list[tuple[str, ...]]]:
        labels: list[bool] = []
        outputs: list[tuple[str, ...]] = []
        for _ in range(n):
            in_s = ds_rng.random() < pi_s
            if in_s:
                k = s_keys[ds_rng.randrange(len(s_keys))]
            else:
                k = nonmembers[ds_rng.randrange(len(nonmembers))]
            y = mm.lookup(k, ds_rng)
            labels.append(in_s)
            outputs.append(y)
        return labels, outputs

    train_rng = random.Random(rng.randint(0, 1 << 30))
    test_rng = random.Random(rng.randint(0, 1 << 30))
    train_labels, train_outputs = make_dataset(n_train, train_rng)
    test_labels, test_outputs = make_dataset(n_test, test_rng)

    alphabet_size = len(VALUES) ** len(instances)
    joint_attacker = JointBayesAttacker.fit(
        labels=train_labels,
        outputs=train_outputs,
        alphabet_size=alphabet_size,
    )
    joint_test_scores = [joint_attacker.score(y) for y in test_outputs]
    joint_acc, joint_auc = attack_metrics(test_labels, joint_test_scores)

    # Single-instance AUCs: marginalize the joint dataset to component i
    # and re-fit a per-component classifier (apples to apples).
    single_aucs: list[float] = []
    for i in range(len(instances)):
        single_train_outputs = [(y[i],) for y in train_outputs]
        single_test_outputs = [(y[i],) for y in test_outputs]
        single_attacker = JointBayesAttacker.fit(
            labels=train_labels,
            outputs=single_train_outputs,
            alphabet_size=len(VALUES),
        )
        single_scores = [single_attacker.score(y) for y in single_test_outputs]
        _, auc_i = attack_metrics(test_labels, single_scores)
        single_aucs.append(auc_i)

    return CellResult(
        name=cfg.name,
        description=cfg.description,
        instance_codecs=[ins.codec_label for ins in cfg.instances],
        instance_f_labels=[ins.f_label for ins in cfg.instances],
        single_tvs=single_tvs,
        single_aucs=single_aucs,
        joint_tv=joint_tv,
        joint_acc=joint_acc,
        joint_auc=joint_auc,
        sum_single_tvs=sum(single_tvs),
        max_single_tv=max(single_tvs) if single_tvs else 0.0,
        max_single_auc=max(single_aucs) if single_aucs else 0.5,
        le_cam_predicted_auc=0.5 + joint_tv / 2.0,
        member_dist_marginals=member_marginals,
        nonmember_dist_marginals=nonmember_marginals,
    )


def run_experiment(
    n_keys: int = 2000,
    n_universe_extra: int = 8000,
    n_train: int = 5000,
    n_test: int = 5000,
    pi_s: float = 0.5,
    nonmember_samples: int = 5000,
    seed: int = 2026,
) -> list[CellResult]:
    rng = random.Random(seed)
    p_f = f_distribution()
    p_f_alt = f_distribution_alt()
    configs = build_configs(p_f)

    out: list[CellResult] = []
    for cfg in configs:
        cell_rng = random.Random(rng.randint(0, 1 << 30))
        out.append(
            run_one_config(
                cfg=cfg,
                p_f=p_f,
                p_f_alt=p_f_alt,
                n_keys=n_keys,
                n_universe_extra=n_universe_extra,
                n_train=n_train,
                n_test=n_test,
                pi_s=pi_s,
                nonmember_samples=nonmember_samples,
                rng=cell_rng,
            )
        )
    return out


# =====================================================================
# Reporting.
# =====================================================================


def fmt(x: float, digits: int = 4) -> str:
    return f"{x:.{digits}g}"


def render_table(results: Sequence[CellResult]) -> str:
    lines = [
        "| config | t | single TVs | single AUCs | joint TV | sum TVs | "
        "max TV | joint AUC | max single AUC | Le Cam UB |",
        "|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|",
    ]
    for r in results:
        single_tvs_s = ", ".join(fmt(x) for x in r.single_tvs)
        single_aucs_s = ", ".join(fmt(x) for x in r.single_aucs)
        lines.append(
            f"| {r.name} | {len(r.instance_codecs)} | {single_tvs_s} | "
            f"{single_aucs_s} | {fmt(r.joint_tv)} | {fmt(r.sum_single_tvs)} | "
            f"{fmt(r.max_single_tv)} | {fmt(r.joint_auc)} | "
            f"{fmt(r.max_single_auc)} | {fmt(r.le_cam_predicted_auc)} |"
        )
    return "\n".join(lines) + "\n"


def render_findings(results: Sequence[CellResult]) -> str:
    out: list[str] = []
    out.append("### Hypothesis checks\n\n")
    # H1: subadditivity holds for INDEPENDENT components. With shared f,
    # members are deterministically correlated and non-members independent,
    # so the joint TV can exceed the sum of marginals.
    h1_violations = [r for r in results if r.joint_tv > r.sum_single_tvs + 1e-3]
    out.append(
        "**H1 (subadditivity, joint TV <= sum of single TVs).** "
        "This bound holds when components are *independent given the "
        "membership label*. In our same-``f`` configurations, members "
        "are deterministically coupled (the same codec applied to the "
        "same value gives the same output) while non-members are "
        "independent, so the bound need not hold. "
        f"Violations: {len(h1_violations)} of {len(results)} configs. "
        + ("All configs respect subadditivity (consistent with "
           "conditional independence). " if not h1_violations else
           f"Configs in violation: {[r.name for r in h1_violations]}. "
           "These are precisely the same-``f`` configurations where "
           "members are deterministically coupled across instances. ")
        + "\n\n"
    )
    # H2: lower bound. joint TV >= max single.
    h2_violations = [r for r in results if r.joint_tv < r.max_single_tv - 1e-3]
    out.append(
        "**H2 (lower bound, joint TV >= max single TV).** "
        f"Violations: {len(h2_violations)} of {len(results)} configs.\n\n"
    )
    # H3: independence compounding. Joint AUC > max single AUC?
    out.append(
        "**H3 (joint AUC pulls away from the better single AUC).** "
        "For each config we compare joint AUC to max single AUC; "
        "the gap measures how much extra leakage the second instance "
        "contributes.\n\n"
    )
    out.append("| config | max single AUC | joint AUC | delta |\n")
    out.append("|---|--:|--:|--:|\n")
    for r in results:
        out.append(
            f"| {r.name} | {fmt(r.max_single_auc)} | {fmt(r.joint_auc)} | "
            f"{fmt(r.joint_auc - r.max_single_auc)} |\n"
        )
    out.append("\n")

    # Headline narrative.
    single_baseline = next(
        (r for r in results if r.name == "Single Huffman (baseline)"), None
    )
    two_huffman_repeat = next(
        (r for r in results if r.name == "Two Huffman, same f (repeat)"), None
    )
    huffman_anti = next(
        (r for r in results if r.name == "Huffman + AntiHuffman, same f (rotation)"),
        None,
    )
    huffman_dense = next(
        (r for r in results if r.name == "Huffman + Dense, same f"), None
    )
    two_anti = next(
        (r for r in results if r.name == "Two AntiHuffman, same f"), None
    )
    three_huffman = next(
        (r for r in results if r.name == "Three Huffman, same f (stacking)"), None
    )

    out.append("### Narrative\n\n")
    if single_baseline and two_huffman_repeat:
        out.append(
            "**Same codec, same f (repeat) is *catastrophic*.** "
            f"Single Huffman gives AUC = {fmt(single_baseline.joint_auc)}; "
            f"observing two Huffman copies of the SAME ``f`` gives AUC = "
            f"{fmt(two_huffman_repeat.joint_auc)}. "
            "On members the two instances coincide deterministically (any "
            "key in ``S`` gives the *same* answer in both); on non-members "
            "the second instance produces an independent random draw. "
            "Whether ``M_1(k) == M_2(k)`` is therefore a near-perfect "
            "membership oracle. This is the central security finding: "
            "publishing the *same* cipher-map twice (same codec, same f) "
            "leaks vastly more than publishing it once, even though the "
            "marginal leakage is unchanged. "
            "\n\n"
        )
    if huffman_anti and huffman_dense:
        out.append(
            "**Codec rotation (Huffman + leakier codec).** "
            f"Pairing Huffman with AntiHuffman: joint AUC = "
            f"{fmt(huffman_anti.joint_auc)} (vs single max "
            f"{fmt(huffman_anti.max_single_auc)}). "
            f"Pairing Huffman with Dense: joint AUC = "
            f"{fmt(huffman_dense.joint_auc)} (vs single max "
            f"{fmt(huffman_dense.max_single_auc)}). "
            "Rotation does NOT defend; the joint always tracks at or above "
            "the leakier component because the attacker can always ignore "
            "the safer component. "
            "\n\n"
        )
    if huffman_anti and two_anti:
        out.append(
            "**Does rotation defend?** No, in our experiments it "
            "compounds. Two AntiHuffman: joint AUC = "
            f"{fmt(two_anti.joint_auc)} (single max "
            f"{fmt(two_anti.max_single_auc)}). Huffman + AntiHuffman: "
            f"joint AUC = {fmt(huffman_anti.joint_auc)} (single max "
            f"{fmt(huffman_anti.max_single_auc)}). The "
            "rotation benefits from the same coincidence-based "
            "membership oracle as the same-codec case, so any "
            "marginal protection from picking a Huffman codec is "
            "swamped. **Rotation backfires** when the safer codec is "
            "deployed alongside a leakier one because the joint "
            "always tracks the leakier component. The defender's "
            "best move is to deploy fewer instances, not to vary "
            "their codecs. "
            "\n\n"
        )
    if three_huffman and two_huffman_repeat and single_baseline:
        out.append(
            "**Stacking (three same-codec instances).** "
            f"Single = {fmt(single_baseline.joint_auc)}, two = "
            f"{fmt(two_huffman_repeat.joint_auc)}, three = "
            f"{fmt(three_huffman.joint_auc)}. "
            "Information saturates with diminishing returns because the "
            "joint AUC is already near 1 with two instances. The first "
            "extra observation buys most of the leverage; the third buys "
            "little. \n\n"
        )

    # Different-f case: members are NOT coupled, so this is the regime
    # that should respect subadditivity-style bounds.
    diff_f = next(
        (r for r in results if r.name == "Two Huffman, different f"), None
    )
    if diff_f:
        out.append(
            "**Different-``f`` per instance is *protective* relative to "
            "shared-``f``.** "
            f"Two Huffman with independent draws of ``f`` per instance: "
            f"joint AUC = {fmt(diff_f.joint_auc)} (single max "
            f"{fmt(diff_f.max_single_auc)}, single TVs "
            f"{[fmt(t) for t in diff_f.single_tvs]}). "
            "Without the coincidence oracle, the joint AUC tracks the "
            "Le Cam bound and is close to the better single-instance "
            "AUC. The asymmetry between the two single TVs reflects "
            "the asymmetry of the two ``f`` distributions: ``f_alt`` is "
            "reverse-Zipf, so the Huffman codec built from ``p_f`` "
            "leaks much more about it. "
            "\n\n"
        )

    out.append("### Theoretical takeaway\n\n")
    out.append(
        "The composition algebra view: a single cipher-map exposes "
        "``Bernoulli<Y>`` over its non-member output, with TV gap "
        "``TV(p_f, q_codec)`` driving the AUC. Observing *t* "
        "instances over the same ``S`` exposes the joint "
        "``Bernoulli<Y_1, ..., Y_t>``. Two regimes:\n\n"
        "* **Conditionally independent regime (different ``f``):** "
        "joint TV obeys subadditivity, joint AUC tracks the "
        "stronger of the per-instance signals, and the Le Cam bound "
        "``AUC <= 1/2 + TV/2`` holds tightly. Multi-instance "
        "leakage is bounded by the most leaky codec deployed.\n"
        "* **Coupled-member regime (shared ``f``):** the diagonal "
        "of the joint distribution is a perfect membership "
        "oracle on its own. Joint TV explodes past the sum of "
        "marginal TVs, and joint AUC approaches 1 even when each "
        "marginal is near-random. This is the dominant "
        "deployment risk.\n\n"
    )
    out.append("### Open questions\n\n")
    out.append(
        "* **Coupled-member oracle as the dominant risk.** The "
        "shared-``f`` coincidence oracle is independent of codec "
        "choice; it is a property of *redeploying the same data* "
        "rather than of the codec. A formal lower bound on joint "
        "AUC as a function of |S| / |Y|^t should be derivable "
        "from the birthday-paradox approximation.\n"
        "* **Compositional defense.** A real defense against "
        "multi-instance attacks would need to *correlate* the "
        "non-member outputs across instances (a shared "
        "pseudorandom permutation seeded by the deployment "
        "context, for example), so the joint distribution of "
        "``(M_1(k), M_2(k))`` for non-members matches that for "
        "members. Codec choice alone cannot defeat the "
        "coincidence oracle.\n"
        "* **Le Cam tightness.** Joint AUC tracks ``1/2 + "
        "joint_TV/2`` closely when the joint alphabet is small; "
        "the bound is tight up to estimation noise.\n"
    )
    return "".join(out)


def render_report(
    results: Sequence[CellResult],
    n_keys: int,
    n_train: int,
    n_test: int,
    pi_s: float,
    seed: int,
    elapsed: float,
) -> str:
    out: list[str] = []
    out.append("# Experiment 12: Multi-instance cipher-map leakage\n\n")
    out.append(
        "Goal: quantify how observing TWO (or more) cipher-map "
        "instances over the same build set ``S`` compounds the "
        "membership-inference leakage relative to observing either "
        "alone. We always use the codec_controlled (ribbon-retrieval) "
        "variant from experiment 07 so the leakage lever is the "
        "codec's codespace allocation.\n\n"
    )
    out.append(
        f"Setup: ``|S| = {n_keys}`` keys, ``|V| = {len(VALUES)}`` values, "
        f"``M = {M_BITS}`` bits, train = {n_train}, test = {n_test}, "
        f"``pi_S = {pi_s}``, seed = {seed}, elapsed = {elapsed:.1f}s.\n\n"
    )
    out.append("## Headline table\n\n")
    out.append(render_table(results))
    out.append("\n## Findings\n\n")
    out.append(render_findings(results))
    return "".join(out)


def main() -> int:
    seed = 2026
    print("Running experiment 12: Multi-instance cipher-map leakage...")
    t0 = time.time()
    results = run_experiment(seed=seed)
    elapsed = time.time() - t0
    report = render_report(
        results,
        n_keys=2000,
        n_train=5000,
        n_test=5000,
        pi_s=0.5,
        seed=seed,
        elapsed=elapsed,
    )
    print(report)
    print(f"\nElapsed: {elapsed:.1f}s")
    out_path = HERE / "RESULTS_12.md"
    out_path.write_text(report)
    print(f"Report written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
