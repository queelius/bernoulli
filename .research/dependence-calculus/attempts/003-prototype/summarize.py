"""Create reproducible tables and scientific plots from the measured artifact."""

from __future__ import annotations

import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from contracts import DNF, degree_two_contract, degree_two_exact


def summarize() -> None:
    root = Path(__file__).resolve().parent
    data = json.loads((root / "benchmark.json").read_text())
    rows = data["results"]
    robust = []
    for n in [8, 12, 16, 128, 1024]:
        q = DNF.from_terms([{i, (i + 1) % n} for i in range(n)])
        contract = degree_two_contract(q, 0.05, 0.2)
        assert contract.zero_sensitivity is not None
        required_alpha = -math.expm1(math.log1p(-0.05) / contract.zero_sensitivity)
        robust.append(
            {
                "sources": n,
                "s0": contract.zero_sensitivity,
                "s1": contract.one_sensitivity,
                "all_false_profile_fpr": degree_two_exact(q, dict.fromkeys(range(n), 0.05)),
                "worst_profile_fpr": contract.fpr_max,
                "worst_profile_fnr_separate_pure_fn_model": contract.fnr_max,
                "alpha_for_query_fpr_005": required_alpha,
            }
        )
    (root / "contract-comparison.json").write_text(json.dumps(robust, indent=2) + "\n")

    fig, axes = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True)
    axes[0].plot(
        [r["sources"] for r in robust],
        [r["all_false_profile_fpr"] for r in robust],
        "o-",
        label="All sources exactly false",
    )
    axes[0].plot(
        [r["sources"] for r in robust],
        [r["worst_profile_fpr"] for r in robust],
        "s--",
        label="Worst exact false-answer profile",
    )
    axes[0].set(
        xscale="log",
        xlabel="Distinct sources in a cycle",
        ylabel="Query false-positive probability",
        title="Same source FPR (5%), different contract",
        ylim=(0, 1.04),
    )
    axes[0].legend(fontsize=8, loc="lower right")
    for method, label in [
        ("exhaustive", "Exhaustive weighted enumeration"),
        ("path_cycle_dp", "Standard path/cycle DP"),
        ("published_symmetric_dissociation", "Published dissociation bounds"),
    ]:
        selected = [
            r
            for r in rows
            if r["case"].startswith("cycle_")
            and r["case"].endswith("_false")
            and r["method"] == method
        ]
        axes[1].plot(
            [r["sources"] for r in selected], [r["median_ms"] for r in selected], "o-", label=label
        )
    axes[1].set(
        xscale="log",
        yscale="log",
        xlabel="Distinct sources in a cycle",
        ylabel="Median inference time (ms)",
        title="Inference cost on synthetic lineages",
    )
    axes[1].legend(fontsize=8)
    for ax in axes:
        ax.grid(alpha=0.2)
    fig.savefig(root / "comparison.svg")
    fig.savefig(root / "comparison.png", dpi=180)
    plt.close(fig)

    estimates = sum(r["kind"] == "estimate" and r["covers_reference"] is False for r in rows)
    failures = sum(r["kind"] != "estimate" and r["covers_reference"] is False for r in rows)
    text = [
        "# Reproducible synthetic results",
        "",
        f"{len(rows)} method/case comparisons; "
        f"{failures} asserted bounds failed reference coverage at tolerance 1e-12. "
        f"Occurrence-product point estimates disagreed in {estimates} cases.",
        "",
        "Times are median milliseconds from three runs unless benchmark metadata says otherwise. "
        "Memory is peak traced allocation during inference, excluding input construction. "
        "These are Python synthetic lineage comparisons, "
        "not compressed-filter or database throughput. "
        "Large cycle reference values use the same standard DP being timed; independent exhaustive "
        "comparison is restricted to small cases. "
        "Dissociation is the symmetric published baseline, "
        "not optimized scaled dissociation.",
        "",
        "| Case | Method | Acceptance interval | ms | Peak bytes |",
        "|---|---|---|---:|---:|",
    ]
    for r in rows:
        if r["case"] in {
            "repeated_and_false",
            "cycle_16_false",
            "cycle_1024_false",
            "shared_hub_128_false",
        } and r["method"] in {
            "occurrence_product",
            "exhaustive",
            "path_cycle_dp",
            "published_symmetric_dissociation",
            "condition_1",
        }:
            text.append(
                f"| {r['case']} | {r['method']} | [{r['acceptance_lower']:.8g}, "
                f"{r['acceptance_upper']:.8g}] | {r['median_ms']:.5g} | {r['peak_traced_bytes']} |"
            )
    text += [
        "",
        "## Truth-uniform one-sided contracts",
        "",
        "Each row uses independent sources with pure false-positive rate 0.05. "
        "The worst profile ranges over all exact assignments making the query false. "
        "The calibration column solves for a source rate that guarantees query FPR at most 0.05. "
        "This is model-level calibration, "
        "not measured storage savings or physical-filter validation.",
        "",
        "| Cycle sources | s0 | All-false profile FPR | Worst-profile FPR | Required source FPR |",
        "|---:|---:|---:|---:|---:|",
    ]
    for r in robust:
        text.append(
            f"| {r['sources']} | {r['s0']} | {r['all_false_profile_fpr']:.7g} | "
            f"{r['worst_profile_fpr']:.7g} | {r['alpha_for_query_fpr_005']:.7g} |"
        )
    text += [
        "",
        "The separate pure-FN model has exact worst FNR 1-(1-0.2)^2=0.36 "
        "for every nontrivial binary-witness cycle, irrespective of its source count. "
        "With both noise types present, these one-sided formulas remain bounds "
        "but are not generally sharp.",
        "",
        "![Contract and inference comparisons](comparison.svg)",
        "",
    ]
    (root / "RESULTS.md").write_text("\n".join(text))
    print(f"Created tables, two plots, and {len(robust)} contract comparisons.")


if __name__ == "__main__":
    summarize()
