A catalogue is stored as a **binary search tree** `root` with distinct values, but after years of inserts it has become lopsided and slow to search.

Return a binary search tree with exactly the same values in which, for every node, the heights of the left and right subtrees differ by **at most one**. If several trees work, return any of them.

{{examples}}

**Constraints**
- The tree has `n` nodes, `1 ≤ n ≤ 10⁴`.
- `-10⁵ ≤ node value ≤ 10⁵`
- The values are distinct, and `root` is a valid binary search tree.
