`root` is a binary search tree with distinct values. Replace every value with **itself plus the sum of all larger values** in the tree. Keep the shape of the tree.

Return the root. Try to use only O(1) extra memory by threading the tree's own empty pointers instead of a stack.

{{examples}}

**Constraints**
- The tree has between `1` and `10⁴` nodes.
- `0 ≤ node value ≤ 10⁴`, all distinct, and `root` is a valid binary search tree.
