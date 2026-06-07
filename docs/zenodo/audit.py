#!/usr/bin/env python3
"""Audit the Zenodo account behind ~/.zenodo.toml.

Lists every deposition (draft and published) the production token can see, with
its direct record URL, so you can actually find DOIs you have minted. Also
reports the numeric owner id of the account the token belongs to, and checks
whether a few known DOIs are present, to detect an account mismatch (uploads
going to a different Zenodo account than the one you log into in the browser).

Reads the token from ~/.zenodo.toml [tokens].production. Never prints the token.

Usage: python3 docs/zenodo/audit.py
"""

from __future__ import annotations

import os
import sys
import urllib.request
import urllib.error
import json

API = "https://zenodo.org/api"
KNOWN = {
    "19104550": "bernoulli_classification_measures (the one DOI you know is yours)",
}


def load_token() -> str:
    path = os.path.join(os.path.expanduser("~"), ".zenodo.toml")
    try:
        import tomllib  # py3.11+
        with open(path, "rb") as f:
            cfg = tomllib.load(f)
    except ModuleNotFoundError:
        import toml
        with open(path, "r", encoding="utf-8") as f:
            cfg = toml.load(f)
    tok = (cfg.get("tokens") or {}).get("production")
    if not tok:
        sys.exit("No [tokens].production in ~/.zenodo.toml")
    return tok


def api_get(path: str, token: str):
    req = urllib.request.Request(f"{API}{path}", headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def main() -> None:
    token = load_token()

    # Pull all depositions (paginate).
    deps = []
    page = 1
    while True:
        batch = api_get(f"/deposit/depositions?size=100&page={page}&all_versions=true", token)
        if not batch:
            break
        deps.extend(batch)
        if len(batch) < 100:
            break
        page += 1

    owners = set()
    print(f"Account behind ~/.zenodo.toml sees {len(deps)} depositions on production zenodo.org\n")
    print(f"{'record_id':<12} {'state':<10} {'DOI':<28} title")
    print("-" * 100)
    for d in sorted(deps, key=lambda x: x.get("id", 0)):
        rid = d.get("id")
        state = "published" if d.get("submitted") else "draft"
        doi = d.get("doi") or (d.get("metadata", {}).get("prereserve_doi", {}) or {}).get("doi") or "-"
        title = (d.get("title") or d.get("metadata", {}).get("title") or "")[:56]
        for o in d.get("owners", []) or []:
            owners.add(o)
        print(f"{rid:<12} {state:<10} {doi:<28} {title}")

    print("-" * 100)
    print(f"\nOwner id(s) of this token's account: {sorted(owners) if owners else 'unknown'}")
    print("Your uploads dashboard for THIS account: https://zenodo.org/me/uploads")
    print("(Open that URL while logged into the account this token belongs to.)\n")

    have = {str(d.get("id")) for d in deps}
    have |= {(d.get("conceptrecid") and str(d.get("conceptrecid"))) for d in deps}
    print("Known-DOI presence check (detects account mismatch):")
    for rid, label in KNOWN.items():
        status = "PRESENT in this account" if rid in have else "NOT in this account"
        print(f"  zenodo.{rid}  {status}  <- {label}")
        # Also fetch the public record to show who owns it.
        try:
            rec = api_get(f"/records/{rid}", token)
            o = rec.get("owners")
            print(f"      public record owner field: {o}")
        except urllib.error.HTTPError as e:
            print(f"      (could not fetch public record {rid}: HTTP {e.code})")


if __name__ == "__main__":
    main()
