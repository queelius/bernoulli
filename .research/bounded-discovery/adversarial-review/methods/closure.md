Targeted closure review, 2026-10-15

Disposition: **M1 closed** in the current manuscript source. No further change is needed for this finding.

Reviewed file: `.research/bounded-discovery/manuscript/body.tex`

SHA-256: `66f0be224c7683c7d8eabfed97dc022e8bbcfca6d5e1b258d2e5d768d6cc414e`

The actual paragraph at lines 233–242 now separately states that a padding word is uniform and independent of the remaining cells, and that fresh independent uniform secret identifier masks make the **recovered suffix** uniform for a singleton or disjoint batch, with the mask vector independent of all identifiers and prefixes. It retains the warning that neither observation proves a complete repair and that the full public view and reuse require analysis.

For any fixed singleton/disjoint history with `c>=1`, the recovered masked suffix is `XOR_i N_i XOR XOR_i M_i`. The stated independent uniform masks make their XOR uniform; independence of the mask vector from the joint identifier/prefix vector preserves this conclusion when conditioning on those identifiers and prefixes. The revision neither claims that masking makes the full word uniform nor that all public observations become private. The original counterexample `P=M` fails the revised prefix-independence premise, and the earlier ambiguous “this statistic” antecedent has been removed.

For padding, conditioning on the remaining cells leaves their XOR fixed; XOR with an independent uniform word is uniform. The retained observation that a genuine occupancy selector can omit padding is consistent with this narrow statistic claim.

The same source explicitly defines public access as visibility to a permissioned-ledger reader (lines 26–32), identifies widths and `kappa` as public configuration (lines 41–42), and qualifies the negative inference about identifying the publisher with “in general” (lines 159–161). Those scope clarifications are compatible with the reviewed arguments and do not change either proposition. This closure does not reopen the broader source or literature audit.

This was a read-only targeted source inspection, followed by writing this closure record. No other reviewer reports were read, no artifact code was changed, and no tests were rerun because the mathematical implementation and tests were unchanged. The original frozen-input report and counterexample evidence remain intact under `methods/`.
