An org chart is a binary tree `root` with distinct employee ids. For two employees with ids `p` and `q`, find their **lowest common manager**: the deepest node that has both `p` and `q` in its subtree. A node counts as being in its own subtree, so if `p` manages `q`, the answer is `p`.

Return that node's id.

{{examples}}

**Constraints**
- The tree has between `2` and `10⁴` nodes.
- `0 ≤ node value ≤ 10⁵`, all distinct.
- `p ≠ q`, and both are in the tree.
