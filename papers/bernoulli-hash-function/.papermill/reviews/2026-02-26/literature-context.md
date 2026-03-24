# Literature Context

## Field Survey: Approximate Membership / Approximate Map Structures

### Core Area
The paper sits at the intersection of **space-efficient probabilistic data structures** and **information-theoretic lower bounds** for approximate set membership (ASM). The canonical reference is Bloom (1970), with the survey by Broder & Mitzenmacher (2004) covering network applications.

### State of the Art in Space-Optimal Filters

1. **Bloom filter** (Bloom 1970): Achieves ~1.44 * (-log2 eps) bits/element. Not space-optimal. No FNR support. No map support.

2. **Compressed Bloom filter** (Mitzenmacher 2002): Compresses Bloom filter for transmission; approaches but does not achieve the lower bound.

3. **Quotient filter** (Bender et al. 2012): Cache-friendly alternative to Bloom; similar space overhead.

4. **Cuckoo filter** (Fan et al. 2014): Practical, supports deletion, achieves roughly (-log2 eps + 3) bits/element for typical configurations.

5. **XOR filter** (Graf & Lemire 2020): Achieves ~1.23 * (-log2 eps) bits/element with O(n) construction time. Very close to optimal in practice.

6. **Ribbon filter** (Dillinger & Walzer 2021): Achieves approximately (-log2 eps + 1.5) bits/element with practical construction. Based on solving random linear systems.

7. **Binary Fuse filter** (Graf & Lemire 2022): Further practical improvement, ~1.125 * (-log2 eps) bits/element.

8. **Retrieval-based filters** (Dietzfelbinger & Pagh 2008; Porat 2009): The theoretical result that exact lower bound (-log2 eps) bits/element is achievable was established by Pagh, Pagh & Rao (2005) and Carter, Floyd, Gill, Markowsky & Wegman (1978). The key insight is that achieving the bound requires exponential construction time or relaxed models.

### Information-Theoretic Lower Bounds

- **Carter et al. (1978)**: Established the n * log2(1/eps) lower bound for membership testers.
- **Pagh, Pagh & Rao (2005)**: Showed the lower bound is tight up to lower-order terms using a retrieval-based approach with polynomial construction.
- **Lovett & Porat (2010)**: Refined lower bounds for dynamic approximate membership.
- **Mitzenmacher & Vadhan (2008)**: Connected optimal hashing to extractors and entropy.

### Order Statistics and Beta Distribution

- **David & Nagaraja (2003)**: The standard reference on order statistics, including the Beta distribution result for uniform order statistics.
- **Arnold, Balakrishnan & Nagaraja (2008)**: First Course in Order Statistics -- alternative reference.
- The result that the k-th order statistic of n i.i.d. Uniform(0,1) is Beta(k, n-k+1) is classical and well-established.

### Random Oracle Model

- **Bellare & Rogaway (1993)**: Formalized the random oracle model. The paper's use of the random oracle assumption is standard in cryptographic and hash-based data structure analysis.

### Approximate Maps

- **Bloomier filter** (Chazelle, Kilian, Rubinfeld & Tal 2004): Function retrieval structure.
- **Retrieval data structures** (Dietzfelbinger & Pagh 2008): Supports arbitrary function storage with near-optimal space.

### Encrypted Search / Oblivious Data Structures

- **Song, Wagner & Perrig (2000)**: Practical techniques for encrypted search.
- **Curtmola, Garay, Kamara & Ostrovsky (2006)**: Searchable symmetric encryption.
- The paper's "obliviousness" claim connects to this literature but is informal.

## Direct Comparisons

### Same Problem (Space-Optimal Approximate Sets)

The BHF's central claim -- achieving exactly -log2(eps) bits/element -- is known to be achievable in principle (Carter et al. 1978 established the bound). The novelty is in the specific hash-based construction mechanism, particularly:

1. The salt-search paradigm (search for a hash seed that makes all elements collide) has appeared in the **perfect hash function** literature (Botelho, Pagh & Ziviani 2007; Czech, Havas & Majewski 1992).

2. The "threshold predicate" generalization is new to this presentation but conceptually related to **locality-sensitive hashing** threshold tests.

3. The **adaptive threshold** variant appears to be novel. Using the p-th order statistic of hash residues as a data-dependent threshold is a new construction, though the underlying order statistic theory is classical.

### Missing Comparisons

The paper does not compare with:
- XOR filters, Ribbon filters, or other modern practical filters
- Cuckoo filters
- The Pagh-Pagh-Rao optimal construction
- Retrieval-based approaches (Dietzfelbinger & Pagh)

These omissions are notable given the paper's claims about achieving the space lower bound.
