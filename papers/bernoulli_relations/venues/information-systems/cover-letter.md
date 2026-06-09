# Cover letter: submission to *Information Systems*

Dear Editors,

Please consider the enclosed manuscript, "The Abstract Data Type of the Approximate
Relation," for publication in *Information Systems*.

**Scope.** Relations are sets of tuples, and a large body of work shows that sets
can be stored far more compactly if one tolerates a controlled error rate (Bloom
filters, perfect hash filters). Reading a relation through such a structure turns an
exact relation into an *approximate* one. This paper asks two questions that have no
off-the-shelf answer: how does per-tuple error propagate through the relational
operators, and when does a structural invariant (reflexivity, symmetry,
single-valuedness, transitivity) survive approximation?

**Contribution.** We model the approximate relation as a Bernoulli random
approximate set over the tuple universe and track error through selection,
projection, and join. The operators behave sharply differently: selection is
rate-transparent, projection amplifies the false-positive rate by its fan-in while
preserving element-wise independence, and a join breaks that independence (output
tuples sharing an input component are correlated). We are explicit that this join
correlation is, in possible-worlds terms, the shared-lineage dependence familiar
from probabilistic databases; we credit that literature and claim only its
closed-form quantification in the representation-error setting. The genuinely new
territory is the invariant side, which culminates in a *closure dichotomy*: an
invariant whose constraints decompose into independent bounded orbits admits a
one-pass repair at a fixed rate cost (a log2(m) bits-per-element surcharge), while
transitivity cascades and admits no bounded repair. The cut is decomposability, not
arity.

**Fit.** *Information Systems* explicitly covers foundational data-management work
from the principal database venues alongside algorithms and data models, without a
systems-implementation requirement, which matches a foundations-of-approximate-
relational-data paper. The work is distinct from probabilistic and uncertain
databases (which model uncertain data tested exactly; here an exact base relation is
tested approximately) and from the consistent-query-answering tradition (whose
dichotomies concern computational complexity, not the rate and space cost of a
repair).

All closed forms are validated by Monte Carlo (a self-contained harness ships with
the paper). The work is original and not under consideration elsewhere; it is part
of a family of preprints on Bernoulli type theory.

Thank you for your consideration.

Alexander Towell
Southern Illinois University Edwardsville
atowell@siue.edu  |  ORCID 0000-0001-6443-9897
