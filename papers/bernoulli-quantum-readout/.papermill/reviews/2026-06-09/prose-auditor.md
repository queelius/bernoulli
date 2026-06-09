# Prose Auditor

**Date**: 2026-06-09
**Scope**: Writing quality of Section 3.6; notation consistency and collisions introduced by it; redundancy with existing material.

## Section 3.6 prose quality

The subsection is well written and well structured: two labeled paragraphs ("The dictionary", "The spectrum") plus an honesty clause. It opens with a clear statement of purpose and a disclaimer of novelty (line 517 to 521), which sets reader expectations correctly. The dictionary/spectrum split is a good rhetorical move. The honesty clause is crisp and pre-empts the obvious misread. Overall it reads at the same level as the rest of the paper.

## Finding P1 (minor), notation collision on the symbol A

**Location**: eq:kron (line 269) and line 504 versus line 534 to 535.
**Quoted text (line 271)**: "Equation~\eqref{eq:kron} is the \emph{assignment matrix} $A$ of readout-error mitigation, in its tensored/local form."
**Quoted text (line 534 to 535)**: "the joint assignment matrix is the Kronecker product $A=\bigotimes_i A_i$, which is \cref{eq:kron} in the column convention".
**Problem**: The symbol `A` is bound to two different matrices that are transposes of each other. At line 269/271/504, `A = Q_1 \otimes ... \otimes Q_n` is the row-stochastic tensor and is already named "the assignment matrix A." At line 535, `A = \bigotimes_i A_i` is the column-stochastic tensor (the `A_i` being transposes of the `Q_i`). Both joint matrices wear the name `A` and both are called "the assignment matrix," even though they are transposes. A careful reader can reconstruct the convention flip from "which is eq:kron in the column convention," but the literal symbol overload is a latent trip hazard, especially since the mitigation literature's `A` is conventionally the column-stochastic one, making the line 271 row-stochastic `A` the non-standard usage.
**Suggestion**: Add one clause at line 534 to 535 disambiguating, e.g. "the joint assignment matrix `A = \bigotimes_i A_i` (the transpose of the row-stochastic `A` of \eqref{eq:kron}; we reuse the name since the two carry the same content)." Or, cleaner, name the column-stochastic joint matrix `A^\top` or `M` to keep the symbols distinct. Severity: minor.

## Finding P2 (minor), "is exactly the assignment matrix ... the transpose"

**Location**: line 523 to 533.
**Quoted text**: "The single-bit readout channel of \cref{def:atom} is exactly the \emph{assignment matrix} (confusion matrix) that readout-error mitigation calibrates and inverts ... it is [eq:assignment] ... the transpose of \cref{eq:channel}."
**Problem**: The sentence asserts the channel "is exactly the assignment matrix" and then displays its *transpose*. Read literally, "is exactly X" followed by "X is the transpose of [the channel]" is mildly self-contradictory at the surface. The intended meaning (the channel and the assignment matrix carry the same information, related by transpose owing to a row-vs-column-stochastic convention) is recoverable, but the word "exactly" overstates given the transpose.
**Suggestion**: Soften to "is the \emph{assignment matrix} (confusion matrix) ... up to the row-vs-column-stochastic convention: written as the mitigation literature prefers it is [eq:assignment], the transpose of \eqref{eq:channel}." Severity: minor.

## Redundancy check with Section 3.4 and related work

No problematic redundancy. Section 3.6 references the parity result rather than re-deriving it, and the overlap with Section 3.4 (parity) and related-work item (c) is intentional and additive: 3.4 proves the identity, item (c) attributes the classical lineage, and 3.6 supplies the operator/spectral reading. The three are complementary views, not duplication. The vonneumann1956/pippenger1988 cites recur across 3.4, 3.6, and (c), which is appropriate (same tradition, three contexts) and not over-citation.

## Notation: r_i, q_i, S_i, F_i

The new subsection reuses `q_i`, `r_i`, `F_i`, `S_i` consistently with their Section 3.4 definitions. The `1-2q_i` / `1-2r_i` usage is consistent with the proof of thm:parity and cor:parity-asym. The one place the prose mislabels `1-2r_i` as an eigenvalue (line 569 to 571) is flagged by logic-checker (L1) as a correctness/wording issue; from a pure prose standpoint it also reads as a slightly over-compressed extension that would benefit from the rewording L1 proposes.

## Verdict
Section 3.6 is clean, purposeful prose that improves the paper. Two minor notation/wording items (P1 symbol-A overload, P2 "is exactly ... the transpose") are worth a light touch. No major prose issue, no narrative regression.
