A binary tree `root` has `n` nodes, and node values are coin counts; there are exactly `n` coins in total. In one **move**, you take one coin from a node and give it to a neighbouring node (its parent or one of its children).

Return the fewest moves needed so that every node holds exactly one coin.

{{examples}}

**Constraints**
- The tree has between `1` and `10⁴` nodes.
- `0 ≤ node value ≤ n`, and the values add up to `n`.
