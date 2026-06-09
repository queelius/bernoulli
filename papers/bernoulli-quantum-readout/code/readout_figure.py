#!/usr/bin/env python3
"""Reproduce the real-device validation figure (sec:worked, fig:realcalib).

Per-qubit asymmetric readout calibration of a real IBM device, taken from the
frozen snapshot that ships with qiskit's fake-provider:

    backend : ibm_hanoi (27 superconducting qubits)
    snapshot: 2025-02-26 calibration
    source  : qiskit_ibm_runtime.fake_provider FakeHanoi properties
              (prob_meas1_prep0 = eps = P[read 1 | prepared 0], a false positive;
               prob_meas0_prep1 = omega = P[read 0 | prepared 1], a false negative)

The snapshot is hardcoded below so the figure reproduces with no network and no
IBM account. To refresh: load FakeHanoi().properties() and read the two fields
per qubit. The omega>eps bias (mean ratio ~2.4) is the T1-relaxation asymmetry.

Outputs: the pgfplots coordinates embedded in main.tex, the headline numbers
quoted in the prose, and a Monte Carlo check that the closed form equals the
simulated parity error on these real rates.
"""
import numpy as np

# (eps_i, omega_i) per qubit, ibm_hanoi, 2025-02-26 snapshot.
RATES = [
    (0.0086, 0.0066), (0.0072, 0.0132), (0.0064, 0.0090), (0.0096, 0.0092),
    (0.0054, 0.0112), (0.0040, 0.0092), (0.0160, 0.0248), (0.0092, 0.0102),
    (0.0092, 0.0144), (0.0022, 0.0238), (0.0284, 0.0200), (0.0340, 0.0500),
    (0.0200, 0.0216), (0.0476, 0.0542), (0.0102, 0.0052), (0.0306, 0.0474),
    (0.0066, 0.0112), (0.0220, 0.0264), (0.0160, 0.0180), (0.0058, 0.0068),
    (0.0042, 0.0068), (0.0076, 0.1610), (0.0090, 0.0174), (0.0132, 0.0182),
    (0.0066, 0.0068), (0.0088, 0.0096), (0.0062, 0.0098),
]

eps = np.array([r[0] for r in RATES])
om = np.array([r[1] for r in RATES])


def forward_exact(rates, n):
    """Closed-form parity-flip probability (Theorem 'Parity'): half of one minus
    the product of the per-bit +/-1 biases 1-2 r_i over the first n ancillas."""
    return 0.5 * (1.0 - np.prod(1.0 - 2.0 * rates[:n]))


def main():
    rng = np.random.default_rng(7)
    ns = list(range(2, len(RATES) + 1))
    cold = [forward_exact(eps, n) for n in ns]          # all ancillas truly |0>, flip rate eps_i
    hot = [forward_exact(om, n) for n in ns]            # all ancillas truly |1>, flip rate omega_i
    lin = [float(np.sum(eps[:n])) for n in ns]          # n-times-per-measurement linearization (cold)

    mc, N = [], 1_000_000                               # Monte Carlo validation of the cold forward value
    for n in ns:
        flips = np.zeros(N, dtype=int)
        for i in range(n):
            flips ^= (rng.random(N) < eps[i]).astype(int)
        mc.append(flips.mean())

    worst = max(abs(m - c) for m, c in zip(mc, cold))
    print(f"omega/eps mean ratio: {(om / eps).mean():.2f}  (T1 readout asymmetry)")
    print(f"formula vs Monte Carlo, worst |diff| over n: {worst:.2e}")
    print(f"n=27: cold={cold[-1]:.3f}, hot={hot[-1]:.3f} (asymmetry gap {hot[-1]-cold[-1]:.3f}); "
          f"linearization overestimates cold by {100*(lin[-1]/cold[-1]-1):.0f}%")
    for name, ys in [("cold", cold), ("mc", mc), ("lin", lin), ("hot", hot)]:
        print(f"%% {name}\n" + " ".join(f"({n},{y:.4f})" for n, y in zip(ns, ys)))


if __name__ == "__main__":
    main()
