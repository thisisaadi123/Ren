A binary tree with distinct values `1..n` was walked in **pre-order** (node, left, right) and **post-order** (left, right, node).

Rebuild **any** binary tree whose two walks are exactly `preorder` and `postorder`. When a node has only one child, the walks can't tell whether it's a left or right child, so either is accepted.

{{examples}}

**Constraints**
- `1 ≤ n ≤ 3 × 10⁴`
- `preorder` and `postorder` are permutations of `1..n` and come from the same tree.
