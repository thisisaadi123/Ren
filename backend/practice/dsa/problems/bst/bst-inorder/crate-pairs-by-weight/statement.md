A warehouse stores crate weights in a binary search tree (for every node, lighter crates on its left side and heavier on its right; all weights are distinct). A truck can carry exactly `target` kilograms of crates, loaded two at a time.

Return how many different pairs of crates weigh exactly `target` together. A pair is two different crates; `(a, b)` and `(b, a)` are the same pair.

{{examples}}

**Constraints**
- The tree has between `1` and `10⁵` nodes and is a valid binary search tree with distinct values.
- `-10⁹ ≤ value ≤ 10⁹`
- `-2 × 10⁹ ≤ target ≤ 2 × 10⁹`
