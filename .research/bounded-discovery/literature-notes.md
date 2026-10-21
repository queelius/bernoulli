# Root literature audit

Checked 2026-10-14. These are scope comparisons, not a claim that every possible
limited-verification deduplication result has already been published.

## Candidate 1, rounds 1–2

- **Dolma official deduplication documentation**: the maintained implementation
  uses a Bloom filter for document attributes or paragraphs, permits false
  positives, and drops tagged duplicates in a later mixer stage. This supports
  the application motivation. Our proposed accepted-document log and immediate
  process-and-insert semantics are a separate application model, not a faithful
  implementation or performance evaluation of Dolma. Source inspected:
  <https://github.com/allenai/dolma/blob/main/docs/deduplication.md>, Deduplication
  and Configuration sections.
- **Bender et al., APOCS 2021, Mitigating False Positives in Filters: to Adapt or
  to Cache?**, DOI 10.1137/1.9781611976489.2. Downloaded author PDF, inspected
  introduction and oracle model. The adaptive filter receives false-positive
  feedback after queries. Extending fingerprints can also fix *other* false
  positives. Consequently a proof that the rescued key becomes a true member
  does not by itself eliminate every possible benefit of adaptive filters.
  Source: <https://cs.uwaterloo.ca/~r27das/zipfian_filters.pdf>.
- **Mo et al., TODS 2026**, same title, DOI 10.1145/3786324. Current indexed
  publisher abstract/introduction states oracle feedback and compares strongly
  adaptive filters with cache-augmented filters. Direct publisher fetch returned
  403; full-text inspection for the mathematical comparison uses the accessible
  2021 predecessor, not a claim of having read the full 2026 journal article.
- **Cesa-Bianchi, Lugosi, Stoltz, IEEE TIT 2005, Minimizing Regret with Label
  Efficient Prediction**, DOI 10.1109/TIT.2005.847729. Downloaded author PDF;
  inspected Sections I–III, including random label requests and importance
  weighting. Fixed label-request budgets and hidden outcomes are established
  models. Their regret target and externally chosen outcomes are not identical
  to distinct-item omissions with an action-dependent processed set.
  Source: <https://stoltz.perso.math.cnrs.fr/Publications/CBLS-LabelEff.pdf>.
- **Jiang et al., AISTATS 2021, Learning the Truth From Only One Side of the
  Story**. Downloaded primary proceedings PDF; inspected Introduction, Related
  Work and model discussion. Selective feedback, sampling bias and randomized
  interventions are already substantive research topics. This work concerns
  generalized linear models, not a theorem settling our specific filter model.
  Source: <https://proceedings.mlr.press/v130/jiang21b/jiang21b.pdf>.
- **Chase and Mehalel, COLT 2025, Deterministic Apple Tasting**. Verified current
  proceedings page and abstract. Feedback observed only for one prediction is
  an established online classification model; this paper sharpens learnability
  and mistake bounds. Only the abstract was inspected, so it is contextual
  prior art rather than a theorem imported into our experiment.
  Source: <https://proceedings.mlr.press/v291/chase25a.html>.
- **Deng and Rafiei, Approximately Detecting Duplicates for Streaming Data**.
  Inspected author full text Sections 1–3: stable Bloom filters deliberately
  forget old elements in a bounded-memory stream and permit both error types.
  Their exact target is prior *arrival*, not prior successful processing; that
  distinction matters for the proposed application. Source:
  <https://webdocs.cs.ualberta.ca/~drafiei/papers/DupDetExt.pdf>.

Downloaded primary PDFs, text extractions and SHA-256 provenance are in
`evidence/`. The extractions are reading aids, not canonical source edits.
