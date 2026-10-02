A tree was written as a string: a node is its value followed by zero, one or two groups in parentheses. The first group is the node's **left** child's subtree and the second group is its **right** child's subtree. An empty left child is written `()` when a right child follows.

Rebuild the tree from `s` and return its root.

{{examples}}

**Constraints**
- `1 ≤ s.length ≤ 3 × 10⁴`
- `s` is a valid encoding of a tree with values between `-1000` and `1000`.
