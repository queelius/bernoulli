# Editorial revision state

Started 2026-10-15 on the author's explicit request for a readable, well-structured,
methodologically sound paper, assessed by multiple independent adversarial agents.

Status: complete. All required editorial, review, verification, and packaging
checks passed. Author scientific review and declarations remain pending.
Three independent reviewers completed initial assessments of readability,
scientific validity against the primary specification, and reproducibility.
They did not read prior favorable reviews or each other's reports before deciding.
Each then challenged the actual revision. The response ledger records findings
and evidence rather than relying on a vote or an undifferentiated approval.

The singleton now leads the argument, followed by a worked example and the
qualified aggregate extension. Shared LaTeX inputs keep canonical and venue
scientific text identical. The table specifies each equality and input class.
The review found and repaired one artifact defect: optimized Python previously
removed assertion-contained insertions. A module-local `__debug__` guard now
fails before results can be generated, including optimized bytecode loaded by
an unoptimized interpreter. Seven artifact tests and ten unchanged scientific tests
pass; full-array mutation checking adds evidence independent of suffix recovery.
Two narrow second-round wording fixes distinguish zero-word occupancy from XOR
and require uniform independent masks for the stated protection.

All three second-round reports close their findings. Both five-page PDFs build
without warnings and all ten rendered pages were inspected. Final source ZIP
builds to identical venue PDF text; final supplement ZIP reproduces every
deterministic result, passes 17 tests, lint and strict typing, and is independently
rechecked. Normal coverage reports 121 statements and 48 branches; rejection
paths are tested separately because `__debug__` is folded at compilation.

Final review bundle: 117 members, all byte-identical to the intended current
sources; nested archives and PDF match verification hashes; all ZIP CRC checks
pass. `validation-final/package-consistency.json` and the venue package manifest
pin that bundle. No further broad revision or test sweep is warranted by the
resolved findings. Next action is the author's review of the five-page draft
and accurate declarations, not another discovery round.

Reviewer agreement is not external peer review and does not prove originality
or editorial acceptance.

Prior manuscripts, package, and verification are saved under `baseline/`.
Unrelated work and previous negative research findings remain out of scope.
No new discovery candidate, broad experiment campaign, external communication,
submission, publication, or expense is authorized here.

Completion requires the evidence listed in `criteria.md`, fresh builds and visual
inspection, coherent supporting artifacts, and a recorded disposition for every
material review finding. Missing author funding/conflict/approval facts remain
explicit; this editorial goal does not authorize inventing declarations.
