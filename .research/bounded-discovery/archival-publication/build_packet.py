"""Build this curated release deterministically; no account data is included."""

from pathlib import Path
import gzip
import hashlib
import io
import json
import tarfile

HERE = Path(__file__).resolve().parent
ROOT = HERE / "stage" / "gbfplus-occupancy-disclosure-v1.0.0"
DEST = HERE / "artifacts"
DEST.mkdir(exist_ok=True)

allowed_suffixes = {".md", ".tex", ".bib", ".cff", ".json", ".txt", ".py", ".pdf"}
files = []
for path in sorted(ROOT.rglob("*")):
    rel = path.relative_to(ROOT)
    if not path.is_file() or any(p.startswith(".") or p == "__pycache__" for p in rel.parts):
        continue
    if path.name == "MANIFEST.json":
        continue
    if path.suffix not in allowed_suffixes and path.name != "Makefile":
        continue
    if path.is_symlink():
        raise ValueError(f"Unexpected link: {rel}")
    files.append(path)

manifest = {
    "schema_version": 1,
    "version": "1.0.0",
    "scope": "Every other regular file in this archive; MANIFEST.json excludes itself.",
    "files": [
        {"path": str(f.relative_to(ROOT)), "bytes": f.stat().st_size,
         "sha256": hashlib.sha256(f.read_bytes()).hexdigest()}
        for f in files
    ],
}
(ROOT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
files.append(ROOT / "MANIFEST.json")
archive = DEST / (ROOT.name + ".tar.gz")
with archive.open("wb") as raw:
    with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode="w", format=tarfile.PAX_FORMAT) as tar:
            for path in sorted(files):
                payload = path.read_bytes()
                info = tarfile.TarInfo(ROOT.name + "/" + str(path.relative_to(ROOT)))
                info.size = len(payload)
                info.mode = 0o644
                info.mtime = 0
                info.uid = info.gid = 0
                info.uname = info.gname = ""
                tar.addfile(info, io.BytesIO(payload))

(DEST / (ROOT.name + ".pdf")).write_bytes((ROOT / "manuscript/main.pdf").read_bytes())
(DEST / "CITATION.cff").write_bytes((ROOT / "CITATION.cff").read_bytes())
artifacts = [
    {"filename": f.name, "bytes": f.stat().st_size,
     "sha256": hashlib.sha256(f.read_bytes()).hexdigest()}
    for f in sorted(DEST.iterdir()) if f.name != "SHA256SUMS" and f.is_file()
]
(DEST / "SHA256SUMS").write_text("".join(f"{f['sha256']}  {f['filename']}\n" for f in artifacts))
checksum = DEST / "SHA256SUMS"
artifacts.append({"filename": checksum.name, "bytes": checksum.stat().st_size,
                  "sha256": hashlib.sha256(checksum.read_bytes()).hexdigest()})
(HERE / "artifact-manifest.json").write_text(json.dumps(artifacts, indent=2) + "\n")
print(json.dumps({"archive": str(archive), "members": len(files), "artifacts": artifacts}, indent=2))
