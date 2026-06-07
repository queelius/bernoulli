#!/usr/bin/env python3
"""Resolve Zenodo record ids to title, version DOI, concept DOI, and record URL.

Reads the production token from ~/.zenodo.toml (never prints it). Give record
ids as arguments:

    python3 docs/zenodo/resolve_dois.py 19105382 19105388 ...
"""

from __future__ import annotations

import os
import sys
import json
import urllib.request

API = "https://zenodo.org/api"


def load_token() -> str:
    path = os.path.join(os.path.expanduser("~"), ".zenodo.toml")
    try:
        import tomllib
        with open(path, "rb") as f:
            cfg = tomllib.load(f)
    except ModuleNotFoundError:
        import toml
        with open(path, "r", encoding="utf-8") as f:
            cfg = toml.load(f)
    return (cfg.get("tokens") or {}).get("production")


def get(path: str, token: str):
    req = urllib.request.Request(f"{API}{path}", headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def main() -> None:
    token = load_token()
    for rid in sys.argv[1:]:
        rec = get(f"/records/{rid}", token)
        md = rec.get("metadata", {})
        title = md.get("title", "?")
        version_doi = rec.get("doi", "?")
        concept_doi = rec.get("conceptdoi", "(none)")
        url = rec.get("links", {}).get("self_html") or f"https://zenodo.org/records/{rid}"
        print(json.dumps({
            "record_id": rid,
            "title": title,
            "version_doi": version_doi,
            "concept_doi": concept_doi,
            "url": url,
        }))


if __name__ == "__main__":
    main()
