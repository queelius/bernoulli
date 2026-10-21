#!/usr/bin/env python3
"""Generate citation/DOI metadata for the bernoulli artifacts from one manifest.

Single source of truth: the ARTIFACTS list below. Running this writes, per
artifact, a CITATION.cff (so GitHub shows a "Cite this repository" box) and,
for the depositable ones, a .zenodo.json (controls the auto-minted Zenodo
record), plus a CC-BY-4.0 LICENSE for the papers that need one. It also
regenerates docs/PROVENANCE.md, the central ledger of repos, licenses, and
DOIs (concept + version).

Edit the manifest, not the generated files. After minting a DOI, paste the
concept and version DOIs into the matching artifact below and re-run.

Usage: python3 docs/zenodo/generate_metadata.py
"""

from __future__ import annotations

import datetime
import json
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

AUTHOR_CFF = (
    "  - family-names: Towell\n"
    "    given-names: Alexander\n"
    '    orcid: "https://orcid.org/0000-0001-6443-9897"\n'
    '    affiliation: "Southern Illinois University Edwardsville"\n'
)
AUTHOR_ZENODO = {
    "name": "Towell, Alexander",
    "orcid": "0000-0001-6443-9897",
    "affiliation": "Southern Illinois University Edwardsville",
}

BASE_KEYWORDS = ["Bernoulli set", "random approximate types", "probabilistic data structure"]

CC_BY_LICENSE = """\
{title}
Copyright (c) 2026 Alexander Towell.

This work is licensed under the Creative Commons Attribution 4.0
International License (CC BY 4.0).

You are free to share (copy and redistribute) and adapt (remix, transform,
and build upon) this material for any purpose, including commercially,
provided you give appropriate credit, link to the license, and indicate if
changes were made.

Full license text: https://creativecommons.org/licenses/by/4.0/legalcode
SPDX-License-Identifier: CC-BY-4.0
"""

# Each artifact: dir (relative to ROOT), repo (github slug), title, type
# (article|book|software), license (SPDX), description, extra keywords,
# write_license (write a CC-BY LICENSE file, overwriting any prior; an optional
# license_note is appended to it, e.g. for embedded code under another license),
# zenodo (emit .zenodo.json), and optional concept_doi / version_doi / url /
# date_released / version, plus manuscript (the dir whose entry in
# papers/freeze-manifest.json describes this artifact, when it differs from
# dir). Frozen papers get their description prefixed from that manifest: the
# freeze date and the superseding monograph chapters.
ARTIFACTS = [
    {
        "dir": "papers/bernoulli_sets", "repo": "bernoulli_sets",
        "title": "Bernoulli sets: a model for random approximate sets",
        "type": "article", "license": "CC-BY-4.0", "write_license": True, "zenodo": True,
        "description": "A probabilistic framework for random approximate sets with independent element-wise false-positive and false-negative errors; two axioms yield the error-count distributions, their normal limits, and confidence intervals.",
        "keywords": ["false positive rate", "false negative rate", "Bloom filter", "axioms"],
        "concept_doi": "10.5281/zenodo.19105381", "version_doi": "10.5281/zenodo.23531295",
        "url": "https://doi.org/10.5281/zenodo.19105381",
    },
    {
        "dir": "papers/bernoulli_composition", "repo": "bernoulli_composition",
        "title": "Composition of Bernoulli sets",
        "type": "article", "license": "CC-BY-4.0", "write_license": True, "zenodo": True,
        "description": "Error rates for complement, union, intersection, and difference of Bernoulli sets, computed per region of the true sets; marginal rate pairs do not compose exactly through nested expressions. Credits independent-event evaluation in probabilistic databases and Bloom-filter set operations.",
        "keywords": ["set composition", "error propagation", "union", "intersection"],
        "concept_doi": "10.5281/zenodo.19105387", "version_doi": "10.5281/zenodo.23531300",
        "url": "https://doi.org/10.5281/zenodo.19105387",
    },
    {
        "dir": "papers/bernoulli_classification_measures", "repo": "bernoulli_classification_measures",
        "title": "Binary classification measures for random approximate sets",
        "type": "article", "license": "CC-BY-4.0", "write_license": True, "zenodo": True,
        "description": "Distributions, expectations, and variances of binary classification measures (PPV, NPV, accuracy, F1, Youden's J) for the Bernoulli set model, via standard delta-method expansions validated by Monte Carlo; no novelty is claimed for the technique.",
        "keywords": ["binary classification", "positive predictive value", "F1-score", "delta method"],
        "concept_doi": "10.5281/zenodo.19104549", "version_doi": "10.5281/zenodo.23531308",
        "url": "https://doi.org/10.5281/zenodo.19104549", "date_released": "2026-03-18",
    },
    {
        "dir": "papers/bernoulli_entropy", "repo": "bernoulli_entropy",
        "title": "Entropy and space complexity of random approximate sets",
        "type": "article", "license": "CC-BY-4.0", "write_license": True, "zenodo": True,
        "description": "The joint entropy of false-positive and false-negative counts in the Bernoulli set model, with an asymptotic expansion, and the space lower bound for approximate membership: the one-sided -log2(epsilon) bound of Carter et al. (1978) and the two-sided bound with false negatives of Pagh and Rodler (2001).",
        "keywords": ["entropy", "space complexity", "information-theoretic bound"],
        "concept_doi": "10.5281/zenodo.20602259", "version_doi": "10.5281/zenodo.23531319",
        "url": "https://doi.org/10.5281/zenodo.20602259", "date_released": "2026-06-08",
    },
    {
        "dir": "papers/bernoulli-hash-function", "repo": "bernoulli-hash-function",
        "title": "The Bernoulli Hash Function: Optimal Bernoulli Sets and Bernoulli Maps",
        "type": "article", "license": "CC-BY-4.0", "write_license": True, "zenodo": True,
        "description": "The Bernoulli hash function (BHF): seed-search constructions of Bernoulli sets and maps whose expected salt length matches the known -log2(epsilon)+mu scale, in exponential expected time, in the lineage of RecSplit and ShockHash. This version corrects the order-statistic law and withdraws the adaptive-threshold space saving.",
        "keywords": ["perfect hash", "fingerprint", "seed search", "succinct data structure"],
        "concept_doi": "10.5281/zenodo.20602261", "version_doi": "10.5281/zenodo.23531320",
        "url": "https://doi.org/10.5281/zenodo.20602261", "date_released": "2026-06-08",
    },
    {
        "dir": "papers/bernoulli-phf", "repo": "bernoulli-phf",
        "title": "The Perfect Hash Filter: An Efficient Implementation of the Positive Bernoulli Set and Bernoulli Map",
        "type": "article", "license": "CC-BY-4.0", "write_license": True, "zenodo": True,
        "description": "The perfect hash filter (PHF): the minimal-perfect-hash-plus-fingerprint filter described by Dietzfelbinger and Pagh (2008), restated as a positive Bernoulli set and map, about log2(e) bits per element above the bound, with a corrected k-perfect false-negative analysis.",
        "keywords": ["perfect hash filter", "succinct data structure", "encrypted search"],
        "concept_doi": "10.5281/zenodo.20602263", "version_doi": "10.5281/zenodo.23531323",
        "url": "https://doi.org/10.5281/zenodo.20602263", "date_released": "2026-06-08",
    },
    {
        "dir": "papers/bernoulli_maps", "repo": "bernoulli_maps",
        "title": "The Algebra of the Random Approximate Map Model",
        "type": "article", "license": "CC-BY-4.0", "write_license": True, "zenodo": True,
        "description": "The Bernoulli map, a probabilistic function generalizing Bernoulli sets to arbitrary codomains, with model order, closed-form marginal rates under composition (element-wise independence holds only without shared intermediate values), and a seed-search construction approaching -log2(epsilon)+mu bits per element.",
        "keywords": ["approximate map", "model order", "composition", "channel"],
        "concept_doi": "10.5281/zenodo.19105389", "version_doi": "10.5281/zenodo.23531328",
        "url": "https://doi.org/10.5281/zenodo.19105389",
    },
    {
        "dir": "papers/bernoulli_relations", "repo": "bernoulli_relations",
        "title": "Error contracts for approximate relations",
        "type": "article", "license": "CC-BY-4.0", "write_license": True, "zenodo": True,
        "description": "Separates exact relation truth, construction randomness, and shared source identity; gives scoped operator and invariant-preservation formulas, one-sided query error contracts, and a stored-filter calibration study. Credits probabilistic relational algebra and probabilistic databases.",
        "keywords": ["approximate relation", "relational algebra", "join", "query error contract"],
        "concept_doi": "10.5281/zenodo.20602265", "version_doi": "10.5281/zenodo.23531330",
        "url": "https://doi.org/10.5281/zenodo.20602265", "date_released": "2026-06-09",
    },
    {
        "dir": "papers/bernoulli_data_type", "repo": "bernoulli_data_type",
        "title": "The Bernoulli Model: A Probabilistic Framework for Data Structures and Types",
        "type": "article", "license": "CC-BY-4.0", "write_license": True, "zenodo": True,
        "description": "An overview of the Bernoulli model of approximate data types: values observed through binary channels with false-positive and false-negative rates, trading space for accuracy. Credits probability-typed approximate computing (Decaf, Rely, Uncertain<T>).",
        "keywords": ["data types", "cipher data types", "error propagation"],
        "concept_doi": "10.5281/zenodo.19105398", "version_doi": "10.5281/zenodo.23531335",
        "url": "https://doi.org/10.5281/zenodo.19105398",
        "manuscript": "papers/bernoulli_data_type/bernoulli_model",
    },
    {
        "dir": "papers/bernoulli_data_type/algebraic_types", "repo": "bernoulli_data_type",
        "title": "Random approximate values over algebraic types",
        "type": "article", "license": "CC-BY-4.0", "write_license": True, "zenodo": True,
        "description": "Random approximate values over algebraic data types (sums, products, functions) with per-type error rates, credited against probability-typed approximate computing (Decaf, Rely, Uncertain<T>, EnerJ, Chisel) and the Giry monad.",
        "keywords": ["algebraic data types", "approximate computing", "probability types"],
        "concept_doi": "10.5281/zenodo.19105395", "version_doi": "10.5281/zenodo.23531336",
        "url": "https://doi.org/10.5281/zenodo.19105395",
        "repo_url_override": "https://github.com/queelius/bernoulli_data_type/tree/main/algebraic_types",
    },
    {
        "dir": "papers/bernoulli-quantum-readout", "repo": "bernoulli-quantum-readout",
        "title": "A Forward (epsilon, omega) Calculus for Quantum Readout Error and the Classical Post-Processing of Measurement Outcomes",
        "type": "article", "license": "CC-BY-4.0", "write_license": True, "zenodo": True,
        "description": "Applies known forward error-propagation tools (signal-probability analysis, probabilistic transfer matrices, Gallager's parity lemma) to Boolean post-processing of asymmetric quantum readout error, computed per latent assignment, with worked ibm_hanoi syndrome-bit numbers. A two-rate pair does not propagate through Boolean trees as a pair.",
        "keywords": ["quantum readout error", "measurement error", "asymmetric channel", "syndrome bit", "error propagation"],
        "concept_doi": "10.5281/zenodo.20584894", "version_doi": "10.5281/zenodo.23531276",
        "url": "https://doi.org/10.5281/zenodo.20584894", "date_released": "2026-06-09",
    },
    {
        "dir": "bernoulli-py", "repo": "bernoulli",
        "title": "bernoulli-types: a Python implementation of random approximate types",
        "type": "software", "license": "MIT", "write_license": False, "zenodo": True,
        "description": "The reference Python implementation of the Bernoulli framework: the atom, sets, maps, relations, sketches, and a composition algebra over error rates.",
        "keywords": ["Python", "Bloom filter", "perfect hash filter", "Count-Min", "HyperLogLog"],
        "repo_url_override": "https://github.com/queelius/bernoulli/tree/main/bernoulli-py",
        "note": "subtree split to queelius/bernoulli-types deferred",
    },
    {
        "dir": "book", "repo": "bernoulli",
        "title": "Bernoulli Types: Two-Sided Error in Approximate Membership, Retrieval, and Computation",
        "type": "book", "license": "CC-BY-4.0", "write_license": True, "zenodo": True,
        "license_note": (
            "Source code embedded in the work (listings and examples) and the companion\n"
            "Python package (bernoulli-py/) are licensed under the MIT License.\n"
        ),
        "description": "A research monograph that organizes approximate membership, retrieval, perfect hashing, sketches, randomized algorithms, approximate relational queries, encrypted search and quantum readout post-processing under one two-rate (false-positive / false-negative) channel model. It credits the established results it unifies, chapter by chapter, states where the model breaks (two-rate summaries do not compose through Boolean formulas; dependence; adaptive queries), and has an executable Python companion, bernoulli-types. It supersedes the author's ten Bernoulli preprints.",
        "keywords": ["monograph", "approximate membership", "two-sided error", "Bloom filter", "perfect hashing", "probabilistic data structures", "approximate computation"],
        "repo_url_override": "https://github.com/queelius/bernoulli/tree/main/book",
        "note": "CC-BY-4.0 chosen 2026-10-21 (embedded code MIT); Zenodo deposit pending the apparatus pass",
    },
]


FREEZE_MANIFEST = os.path.join(ROOT, "papers", "freeze-manifest.json")


def _freeze_manifest() -> dict:
    """papers/freeze-manifest.json, or an empty manifest if the papers are not frozen."""
    try:
        with open(FREEZE_MANIFEST, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"manuscripts": []}


def _chapters_phrase(chapters: list[int]) -> str:
    nums = [str(c) for c in chapters]
    if len(nums) == 1:
        return f"Chapter {nums[0]}"
    return "Chapters " + ", ".join(nums[:-1]) + " and " + nums[-1]


def description(a: dict) -> str:
    """The deposit description: frozen papers lead with the freeze and the superseding chapters."""
    manifest = _freeze_manifest()
    entries = {m["dir"]: m for m in manifest["manuscripts"]}
    entry = entries.get(a.get("manuscript", a["dir"]))
    if entry is None:
        return a["description"]
    frozen = datetime.date.fromisoformat(manifest["generated"]).strftime("%B %Y")
    book = next(x for x in ARTIFACTS if x["type"] == "book")
    chapters = _chapters_phrase([c["chapter"] for c in entry["monograph_chapters"]])
    return (
        f"Final version ({frozen}), with errata; superseded by the monograph "
        f"{book['title']}, {chapters}. " + a["description"]
    )


def repo_url(a: dict) -> str:
    return a.get("repo_url_override", f"https://github.com/queelius/{a['repo']}")


def write_citation_cff(a: dict) -> None:
    kws = BASE_KEYWORDS + a.get("keywords", [])
    lines = [
        "cff-version: 1.2.0",
        'message: "If you use this work, please cite it as below."',
        f'title: "{a["title"]}"',
        f"type: {a['type']}",
        "authors:",
        AUTHOR_CFF.rstrip("\n"),
        f'repository-code: "{repo_url(a)}"',
    ]
    if a["license"] != "all-rights-reserved":
        lines.append(f"license: {a['license']}")
    if a.get("version_doi"):
        lines.append(f'doi: "{a["version_doi"]}"')
    if a.get("url"):
        lines.append(f'url: "{a["url"]}"')
    if a.get("date_released"):
        lines.append(f'date-released: "{a["date_released"]}"')
    lines.append("keywords:")
    lines += [f"  - {k}" for k in kws]
    path = os.path.join(ROOT, a["dir"], "CITATION.cff")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def write_zenodo_json(a: dict) -> None:
    if not a.get("zenodo"):
        return
    rec: dict = {
        "title": a["title"],
        "upload_type": "software" if a["type"] == "software" else "publication",
        "description": description(a),
        "creators": [AUTHOR_ZENODO],
        "keywords": BASE_KEYWORDS + a.get("keywords", []),
        "license": a["license"],
        "access_right": "open",
    }
    if rec["upload_type"] == "publication":
        rec["publication_type"] = "book" if a["type"] == "book" else "article"
    path = os.path.join(ROOT, a["dir"], ".zenodo.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=2)
        f.write("\n")


def write_license(a: dict) -> None:
    if not a.get("write_license"):
        return
    path = os.path.join(ROOT, a["dir"], "LICENSE")
    with open(path, "w", encoding="utf-8") as f:
        f.write(CC_BY_LICENSE.format(title=a["title"]))
        if a.get("license_note"):
            f.write("\n" + a["license_note"])


def write_provenance() -> None:
    rows = []
    for a in ARTIFACTS:
        concept = a.get("concept_doi") or "(mint)"
        version = a.get("version_doi") or "(mint)"
        status = "DOI minted" if a.get("version_doi") else "metadata ready"
        note = f" {a['note']}" if a.get("note") else ""
        rows.append(
            f"| {a['title']} | [{a['repo']}]({repo_url(a)}) | {a['type']} | "
            f"{a['license']} | {concept} | {version} | {status}{note} |"
        )
    body = f"""# Provenance and DOIs

Single source of truth for the bernoulli artifacts: repos, licenses, and Zenodo
DOIs (concept + version). Generated by `docs/zenodo/generate_metadata.py` from
its manifest. Edit the manifest and re-run; do not hand-edit this file.

| Artifact | Repo | Type | License | Concept DOI | Latest version DOI | Status |
|---|---|---|---|---|---|---|
{chr(10).join(rows)}

## Licensing policy
- Papers: CC-BY-4.0 (the two formerly GPL-3.0 papers, sets and data_type, were harmonized).
- `bernoulli-py`: MIT.
- Monograph: CC-BY-4.0 (decided 2026-10-21); embedded code samples and the companion package are MIT.

## Minting a DOI (one-time per repo)
1. Sign in at https://zenodo.org with GitHub and authorize it.
2. In Zenodo's GitHub settings, switch the repo ON.
3. Create a tagged GitHub release (e.g. `v1.0.0`). Zenodo archives the release
   and mints a version DOI plus a version-agnostic concept DOI.
4. Paste both DOIs into the artifact's entry in
   `docs/zenodo/generate_metadata.py`, re-run it, and commit.

The `.zenodo.json` in each repo controls the deposit metadata; `CITATION.cff`
makes GitHub render a "Cite this repository" box and is read by Zenodo too.
"""
    with open(os.path.join(ROOT, "docs", "PROVENANCE.md"), "w", encoding="utf-8") as f:
        f.write(body)


def main() -> None:
    for a in ARTIFACTS:
        write_citation_cff(a)
        write_zenodo_json(a)
        write_license(a)
    write_provenance()
    n_cff = len(ARTIFACTS)
    n_zen = sum(1 for a in ARTIFACTS if a.get("zenodo"))
    n_lic = sum(1 for a in ARTIFACTS if a.get("write_license"))
    print(f"wrote {n_cff} CITATION.cff, {n_zen} .zenodo.json, {n_lic} CC-BY LICENSE, 1 PROVENANCE.md")


if __name__ == "__main__":
    main()
