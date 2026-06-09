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
# write_license (write a CC-BY LICENSE file, overwriting any prior),
# zenodo (emit .zenodo.json), and optional concept_doi / version_doi / url /
# date_released / version. bernoulli-quantum-readout is intentionally absent
# (drafted separately); add it once it exists.
ARTIFACTS = [
    {
        "dir": "papers/bernoulli_sets", "repo": "bernoulli_sets",
        "title": "Bernoulli sets: a model for random approximate sets",
        "type": "article", "license": "CC-BY-4.0", "write_license": True, "zenodo": True,
        "description": "A probabilistic framework for random approximate sets with independent element-wise false-positive and false-negative errors; two axioms yield the error-count distributions, their normal limits, and confidence intervals.",
        "keywords": ["false positive rate", "false negative rate", "Bloom filter", "axioms"],
        "concept_doi": "10.5281/zenodo.19105381", "version_doi": "10.5281/zenodo.19105382",
        "url": "https://doi.org/10.5281/zenodo.19105381",
    },
    {
        "dir": "papers/bernoulli_composition", "repo": "bernoulli_composition",
        "title": "Composition of Bernoulli sets",
        "type": "article", "license": "CC-BY-4.0", "write_license": True, "zenodo": True,
        "description": "Closed-form error rates for complement, union, intersection, and difference of Bernoulli sets, showing the model is closed under set-theoretic composition.",
        "keywords": ["set composition", "error propagation", "union", "intersection"],
        "concept_doi": "10.5281/zenodo.19105387", "version_doi": "10.5281/zenodo.19105388",
        "url": "https://doi.org/10.5281/zenodo.19105387",
    },
    {
        "dir": "papers/bernoulli_classification_measures", "repo": "bernoulli_classification_measures",
        "title": "Binary classification measures for random approximate sets",
        "type": "article", "license": "CC-BY-4.0", "write_license": True, "zenodo": True,
        "description": "Distributions, expectations, and variances of binary classification measures (PPV, NPV, accuracy, F1, Youden's J) for the Bernoulli set model, via delta-method expansions validated by Monte Carlo.",
        "keywords": ["binary classification", "positive predictive value", "F1-score", "delta method"],
        "concept_doi": "10.5281/zenodo.19104549", "version_doi": "10.5281/zenodo.19104550",
        "url": "https://doi.org/10.5281/zenodo.19104549", "date_released": "2026-03-18",
    },
    {
        "dir": "papers/bernoulli_entropy", "repo": "bernoulli_entropy",
        "title": "Entropy and space complexity of random approximate sets",
        "type": "article", "license": "CC-BY-4.0", "write_license": True, "zenodo": True,
        "description": "The joint entropy of false-positive and false-negative counts in the Bernoulli set model, with a closed-form asymptotic expansion and the -log2(epsilon) bits-per-element space bound.",
        "keywords": ["entropy", "space complexity", "information-theoretic bound"],
        "concept_doi": "10.5281/zenodo.20602259", "version_doi": "10.5281/zenodo.20602260",
        "url": "https://doi.org/10.5281/zenodo.20602259", "date_released": "2026-06-08",
    },
    {
        "dir": "papers/bernoulli-hash-function", "repo": "bernoulli-hash-function",
        "title": "The Bernoulli Hash Function: Optimal Bernoulli Sets and Bernoulli Maps",
        "type": "article", "license": "CC-BY-4.0", "write_license": True, "zenodo": True,
        "description": "The Bernoulli hash function (BHF): hash-based constructions that optimally implement the Bernoulli set and map at the information-theoretic space bound.",
        "keywords": ["perfect hash", "fingerprint", "space-optimal", "succinct data structure"],
        "concept_doi": "10.5281/zenodo.20602261", "version_doi": "10.5281/zenodo.20602262",
        "url": "https://doi.org/10.5281/zenodo.20602261", "date_released": "2026-06-08",
    },
    {
        "dir": "papers/bernoulli-phf", "repo": "bernoulli-phf",
        "title": "The Perfect Hash Filter: An Efficient Implementation of the Positive Bernoulli Set and Bernoulli Map",
        "type": "article", "license": "CC-BY-4.0", "write_license": True, "zenodo": True,
        "description": "The perfect hash filter (PHF): a practical static positive Bernoulli set built by off-the-shelf minimal perfect hashing, approaching the -log2(epsilon) bits-per-element bound to within a constant log2(e), and extended to the perfect hash map; the deployable counterpart to the space-optimal Bernoulli hash function.",
        "keywords": ["perfect hash filter", "succinct data structure", "encrypted search"],
        "concept_doi": "10.5281/zenodo.20602263", "version_doi": "10.5281/zenodo.20602264",
        "url": "https://doi.org/10.5281/zenodo.20602263", "date_released": "2026-06-08",
    },
    {
        "dir": "papers/bernoulli_maps", "repo": "bernoulli_maps",
        "title": "The Algebra of the Random Approximate Map Model",
        "type": "article", "license": "CC-BY-4.0", "write_license": True, "zenodo": True,
        "description": "The Bernoulli map, a probabilistic function generalizing Bernoulli sets to arbitrary codomains, with model order, the composition theorem, and a space-optimal construction at -log2(epsilon)+mu bits per element.",
        "keywords": ["approximate map", "model order", "composition theorem", "channel"],
        "concept_doi": "10.5281/zenodo.19105389", "version_doi": "10.5281/zenodo.19105390",
        "url": "https://doi.org/10.5281/zenodo.19105389",
    },
    {
        "dir": "papers/bernoulli_relations", "repo": "bernoulli_relations",
        "title": "The Abstract Data Type of the Approximate Relation",
        "type": "article", "license": "CC-BY-4.0", "write_license": True, "zenodo": True,
        "description": "The approximate relation, a probabilistic relation with false and complementary-false correspondences; error propagation through join and project, an approximate-set-based implementation, and a trapdoor-database application.",
        "keywords": ["approximate relation", "relational algebra", "join", "trapdoor database"],
        "concept_doi": "10.5281/zenodo.20602265", "version_doi": "10.5281/zenodo.20602266",
        "url": "https://doi.org/10.5281/zenodo.20602265", "date_released": "2026-06-08",
    },
    {
        "dir": "papers/bernoulli_data_type", "repo": "bernoulli_data_type",
        "title": "The Bernoulli Model: A Probabilistic Framework for Data Structures and Types",
        "type": "article", "license": "CC-BY-4.0", "write_license": True, "zenodo": True,
        "description": "The Bernoulli Model, a probabilistic framework for uncertainty in data types, trading space for accuracy with O(1) operations and probabilistic guarantees; the foundational overview.",
        "keywords": ["data types", "cipher data types", "Count-Min sketch", "error propagation"],
        "concept_doi": "10.5281/zenodo.19105398", "version_doi": "10.5281/zenodo.19105399",
        "url": "https://doi.org/10.5281/zenodo.19105398",
        "note": "algebraic_types sub-paper minted separately at concept 10.5281/zenodo.19105395 (version 10.5281/zenodo.19105396)",
    },
    {
        "dir": "papers/bernoulli-quantum-readout", "repo": "bernoulli-quantum-readout",
        "title": "A Forward (epsilon, omega) Calculus for Quantum Readout Error and the Classical Post-Processing of Measurement Outcomes",
        "type": "article", "license": "CC-BY-4.0", "write_license": True, "zenodo": True,
        "description": "A reusable, forward, asymmetric calculus that propagates a false-positive/false-negative rate pair through Boolean combinations and Kronecker composition of measured qubits, unifying a quantum readout-error model with the Bernoulli theory of approximate sets and maps.",
        "keywords": ["quantum readout error", "measurement error", "asymmetric channel", "syndrome bit", "error propagation"],
        "concept_doi": "10.5281/zenodo.20584894", "version_doi": "10.5281/zenodo.20586587",
        "url": "https://doi.org/10.5281/zenodo.20584894", "date_released": "2026-06-07",
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
        "title": "Bernoulli Types: An Algebra of Approximate Computation",
        "type": "book", "license": "all-rights-reserved", "write_license": False, "zenodo": False,
        "description": "A research monograph synthesizing the Bernoulli framework for random approximate types (sets, maps, relations, algebraic types) with an executable Python companion.",
        "keywords": ["monograph", "approximate computation", "type theory"],
        "repo_url_override": "https://github.com/queelius/bernoulli/tree/main/book",
        "note": "all-rights-reserved (KDP-bound); Zenodo deposit + repo split deferred",
    },
]


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
        "description": a["description"],
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
- Monograph: all-rights-reserved for now (Amazon KDP intent); revisit before any Zenodo deposit.

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
