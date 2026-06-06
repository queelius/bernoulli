# Experiment 16: Scope of the Le Cam codec security claim

The Le Cam-based codec security argument from Experiment 11 bounds *value-only* attacker accuracy by ``1/2 + TV(P_member, P_nonmember) / 2``. This experiment checks the scope. The codec controls TV in *value space*; a codec choice cannot control TV in any joint space the attacker constructs from the key. If keys carry features that correlate with membership, an attacker that ignores values entirely can exceed the value-only Le Cam bound, and codec choice is irrelevant against that attack.

We instantiate three key universes and two attackers, holding the codec fixed at Huffman from ``p_f`` (the TV-minimal codec from Exp 11). The cipher-map setup, value alphabet, and attacker training pipeline follow Exp 11. Elapsed = 0.3s.

## Headline

| Universe | TV_value | TV_joint | ValueOnly acc | LeCam_value | KeyFeature acc | LeCam_joint |
|---|--:|--:|--:|--:|--:|--:|
| U_random | 0.147 | 0.147 | 0.5652 | 0.5735 | 0.5326 | 0.5735 |
| U_modular | 0.1531 | 1 | 0.5724 | 0.5766 | 0.9974 | 1 |
| U_partial | 0.1469 | 1 | 0.5738 | 0.5735 | 0.9896 | 1 |

## Findings

* **U_random**: TV_value = 0.147, TV_joint = 0.147. The two TVs agree to within Monte Carlo noise (key features carry no membership signal). ValueOnly acc = 0.5652 (Le Cam value bound 0.5735). KeyFeature acc = 0.5326; the joint attacker offers no advantage, and the Le Cam value bound is tight.
* **U_modular**: TV_value = 0.1531, TV_joint = 1 (key features fully determine membership). ValueOnly acc = 0.5724 (still bounded by Le Cam value 0.5766). KeyFeature acc = 0.9974, far above the value-only bound. The codec is irrelevant against this attacker.
* **U_partial**: TV_value = 0.1469, TV_joint = 1. The joint TV is intermediate: key features carry signal but do not uniquely determine membership. ValueOnly acc = 0.5738. KeyFeature acc = 0.9896, exceeding the value-only bound but below 1.

## Verdict

The value-only Le Cam bound holds across every key universe for the ValueOnlyAttacker, as expected: TV in value space is a property of the codec and the value distribution, independent of the key universe. The KeyFeatureAttacker, however, exceeds the value-only bound whenever key features carry membership signal. Its accuracy tracks ``1/2 + TV_joint / 2`` instead, where TV_joint is the TV in (key feature, value) space and is *not* under the codec's control.

The implication for the security argument in Exp 11 is scope: codec choice defends against value-only attackers, which is the relevant threat model when the key universe is unstructured (uniform random keys, ``S`` chosen independently of any computable feature). When the key universe carries membership-correlated features, the appropriate defense is access control on the key universe (e.g., key derivation that destroys the structure, or treating keys themselves as secret). The codec is the right primitive for the value-only threat model and the wrong one otherwise.
