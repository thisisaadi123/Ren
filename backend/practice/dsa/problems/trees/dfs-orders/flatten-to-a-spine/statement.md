Rearrange a binary tree **in place** into a single spine: every node's left child becomes empty, and following right children from the root visits the nodes in pre-order (a node, then its whole left branch in pre-order, then its whole right branch in pre-order).

Return the root of the spine (the same root as before, or an empty tree if the tree was empty).

{{examples}}

**Constraints**
- The tree has between `0` and `10⁵` nodes.
- `-1000 ≤ value ≤ 1000`
