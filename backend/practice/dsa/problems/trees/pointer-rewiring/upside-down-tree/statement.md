In the binary tree `root`, every right child is a **leaf** that has a left sibling (or there is no right child at all). Turn the tree **upside down**, one level at a time:

1. The original left child becomes the new root.
2. The original root becomes the new root's **right** child.
3. The original right child becomes the new root's **left** child.

Apply this all the way down the left edge, so the bottom-left node ends up as the root. Return the new root.

{{examples}}

**Constraints**
- The tree has between `0` and `10⁴` nodes.
- `1 ≤ node value ≤ 10⁴`
- Every right child is a leaf with a left sibling.
