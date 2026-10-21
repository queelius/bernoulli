# Independent critical review

Reviewer: a separate research agent, `/root/publication_review`, 2026-10-14.
This is computational and critical assistance, not external peer review or
endorsement by the target journal. The reviewer was read-only and did not
write the main proof, implementation, or manuscript.

## Premise and publication screen

The reviewer independently inspected the saved publisher paper and identified:

- §4.2 p.7 and Table 1 p.4: the adjacent-domain confidentiality goal.
- §5.1 p.9: public domain-ID associations.
- §5.2 pp.10–11: timeout finalization without a specified minimum count and
  publication of full filter/count in the transaction following Eq.(5).
- Algorithm 4 p.11: κ distinct positions and XOR target `prefix || N_adj`.
- §6.2 p.18: public occupancy and sparse storage.

It found no padding, payload encryption, minimum-count rule, or access
restriction in the specified public ledger view that defeats the singleton
case. Paillier concerns enrollment; signatures authenticate the exposed data.

The reviewer accepted both the singleton identity and the sufficient condition
`w=cκ` for disjoint supports. It insisted on endpoint/suffix disclosure rather
than identifier-game break, signer identification, raw-data recovery, or a
complete path. It also checked that digest/signature equality must not be
part of the equal-structural-metadata premise.

Verdict: a plausible short conventional Comment correcting a concrete
published confidentiality goal. The elementary XOR mathematics is not the
claimed novelty. Original GBF padding and OT access are a necessary contrast;
no complete repair follows merely from hiding occupancy or adding a mask.

## Independent implementation check

The reviewer reran the first 15 tests and measured 100% statement/branch
coverage for `gbfplus_probe.py` and `joint_probe.py` in memory. It separately
enumerated all small updates over three cells with two-bit words, comparing
the produced arrays to all arrays consistent with existing occupied cells
and the new XOR equation:

- 2,844 successful configurations: exactly all feasible arrays, each once.
- 4,656 fully occupied configurations: atomic failure, no mutation.

This additional enumeration was executed by the independent agent in memory;
it is supplementary corroboration. The durable root tests and reproducible
driver, not an unavailable reviewer script, support the manuscript's counts.

It found no material code defect. It noted that `insert()` does not enforce
capacity, maintain count, rotate/finalize, derive tokens or sign; the driver
and manuscript must preserve that distinction. Authentic count and honest
history remain premises, not consequences of `Snapshot` input validation.

## Draft and artifact review

The reviewer read `manuscript/main.tex`, bibliography, driver and saved results.
All 19 current tests passed. A fresh `reproduce()` matched every deterministic
JSON field and recorded source hash; descriptive scan timing was excluded.
The five-page build had no unresolved citations/references or overflow after
the path layout fix.

No scientific blocker was found. Three requested corrections were accepted:

1. Attribute Eq.(27) as an analysis under its random-share model, rather than
   unconditionally endorsing the source bound. **Applied.**
2. Say the counterexample premises were checked against the published
   specification, not imply an end-to-end scheduler/cryptography verification.
   **Applied.**
3. Add runnable artifact instructions and mark the unimplemented HMAC wrapper
   discussion as historical planning. **README added; model plan labeled and
   actual delivered modules/scope recorded.**

Final recommendation: **GO for a focused conventional Comment; no broad
theory/security-paper claim.** Remaining author review and venue adaptation
plausibly fit one week. Actual journal acceptance, fee exemption, and PhD credit
remain unverified and require the author's later decisions.
