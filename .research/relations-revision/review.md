# Independent review and dispositions

Reviewed 2026-10-13 by an independent read-only review agent; root integrated fixes.

The reviewer found the main boundary contracts, heterogeneous and marginal-only
bounds, shared-rate Jensen proof, source covariance, corrected single-valuedness,
and restricted transitivity statements sound under their explicit models.
Amarilli–Monet Section 6 independently supports the edge-cover counting citation.

| Finding | Disposition |
|---|---|
| Worked example referenced tables removed from preliminaries | Replaced with explicit small relations in the operator section. |
| Projection proof described the direction of dropping product factors incorrectly | Reworded to including factors decreases the product and increases its complement. |
| Paper claimed mode stored in a 40-byte header | Corrected: mode is external query context; bytes count Bloom header and payload. |
| Float acceptance is not generally exact certification | Separate integer/Fraction audit checks every recorded build. Generic limitation retained. |
| Tiny-rate OR and cycle calculations rounded positive probabilities to zero | Regression cases reproduced; experiment worker replaced cancellation-prone formulas and reran experiment. Final verification recorded separately. |
| 55.8% saving could be misread as sharp-contract benefit | Added conservative sizing baseline: 3,768 versus 3,752 bytes; explicit attribution to representative count and repair cost. |

Independent exact audit covered all 480 build rows, including 320 calibrated
query envelopes. It found no ideal-model target violation and confirmed the
recorded implementation digest before the numerical revision. The final rerun
and audit must be checked together; see `validation.md`.

Review verdict: a defensible working synthesis and reproducible calibration
study, with insufficient evidence yet for a substantial original research paper.
