#!/usr/bin/env python3
"""Mint a Zenodo deposit for a paper, driven by its .zenodo.json.

The packaged zenodo-upload CLI only sets title/description/creators and drops
license and publication_type. This minter reads the full .zenodo.json that the
repo already maintains and sets correct article metadata, then uploads the PDF.

Two-step by design so the irreversible publish is deliberate:

    python3 docs/zenodo/mint.py draft   papers/<dir> <pdf>   # create + upload + metadata, NO publish
    python3 docs/zenodo/mint.py show    <deposition_id>      # inspect a draft
    python3 docs/zenodo/mint.py publish <deposition_id>      # irreversible: mint the DOI

Token: ~/.zenodo.toml [tokens].production (never printed). Production zenodo.org.
"""

from __future__ import annotations

import os
import sys
import json
import urllib.request
import urllib.error

API = "https://zenodo.org/api"

# Map our .zenodo.json license string to the Zenodo license id.
LICENSE_ID = {"CC-BY-4.0": "cc-by-4.0", "MIT": "mit", "cc-by-4.0": "cc-by-4.0"}


def token() -> str:
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


def _req(method: str, url: str, tok: str, data=None, ctype="application/json"):
    headers = {"Authorization": f"Bearer {tok}"}
    body = None
    if data is not None:
        if ctype == "application/json":
            body = json.dumps(data).encode()
            headers["Content-Type"] = "application/json"
        else:
            body = data  # raw bytes for file upload
            headers["Content-Type"] = ctype
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r) if r.length != 0 else {}
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code} on {method} {url}\n{e.read().decode(errors='replace')}")


def build_metadata(paper_dir: str) -> dict:
    z = json.load(open(os.path.join(paper_dir, ".zenodo.json"), encoding="utf-8"))
    md = {
        "upload_type": z.get("upload_type", "publication"),
        "title": z["title"],
        "description": z["description"],
        "creators": z["creators"],
        "keywords": z.get("keywords", []),
        "access_right": z.get("access_right", "open"),
        "license": LICENSE_ID.get(z.get("license", ""), "cc-by-4.0"),
    }
    if md["upload_type"] == "publication":
        md["publication_type"] = z.get("publication_type", "article")
    return md


def draft(paper_dir: str, pdf_path: str) -> None:
    tok = token()
    md = build_metadata(paper_dir)
    filename = os.path.basename(paper_dir.rstrip("/")) + ".pdf"

    print(f"Creating deposition for: {md['title']}")
    dep = _req("POST", f"{API}/deposit/depositions", tok, data={})
    dep_id = dep["id"]
    bucket = dep["links"]["bucket"]
    reserved = (dep.get("metadata", {}).get("prereserve_doi") or {}).get("doi", "?")
    print(f"  deposition id: {dep_id}")
    print(f"  reserved DOI:  {reserved}")

    print(f"Uploading {pdf_path} as {filename} ...")
    with open(pdf_path, "rb") as f:
        _req("PUT", f"{bucket}/{filename}", tok, data=f.read(), ctype="application/octet-stream")
    print("  file uploaded")

    print("Setting metadata from .zenodo.json ...")
    final = _req("PUT", f"{API}/deposit/depositions/{dep_id}", tok, data={"metadata": md})
    m = final["metadata"]
    print("  metadata echo:")
    print(f"    title:            {m.get('title')}")
    print(f"    upload_type:      {m.get('upload_type')} / {m.get('publication_type')}")
    print(f"    license:          {m.get('license')}")
    print(f"    creators:         {[c.get('name') for c in m.get('creators', [])]}")
    print(f"    access_right:     {m.get('access_right')}")
    print(f"    files:            {[f['filename'] for f in final.get('files', [])]}")
    print(f"\n  DRAFT ready (NOT published). Reserved DOI: {reserved}")
    print(f"  Review:  {final['links'].get('latest_draft_html', final['links'].get('html'))}")
    print(f"  Publish: python3 docs/zenodo/mint.py publish {dep_id}")


def show(dep_id: str) -> None:
    tok = token()
    dep = _req("GET", f"{API}/deposit/depositions/{dep_id}", tok)
    m = dep.get("metadata", {})
    print(json.dumps({
        "id": dep["id"],
        "state": "published" if dep.get("submitted") else "draft",
        "doi": dep.get("doi") or (m.get("prereserve_doi") or {}).get("doi"),
        "title": m.get("title"),
        "license": m.get("license"),
        "publication_type": m.get("publication_type"),
        "files": [f["filename"] for f in dep.get("files", [])],
    }, indent=2))


def publish(dep_id: str) -> None:
    tok = token()
    res = _req("POST", f"{API}/deposit/depositions/{dep_id}/actions/publish", tok, data={})
    print("PUBLISHED")
    print(f"  DOI:            {res.get('doi')}")
    print(f"  concept DOI:    {res.get('conceptdoi')}")
    print(f"  record:         {res.get('links', {}).get('record_html')}")


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cmd = sys.argv[1]
    if cmd == "draft":
        draft(sys.argv[2], sys.argv[3])
    elif cmd == "show":
        show(sys.argv[2])
    elif cmd == "publish":
        publish(sys.argv[2])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
