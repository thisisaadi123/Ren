Trace the outline of a binary tree `root` counter-clockwise, starting at the root, and return the values in that order:

1. The **root**.
2. The **left edge**, top to bottom: start at the root's left child (if there is none, the left edge is empty), then keep stepping to the left child when there is one and to the right child otherwise. Leaves aren't part of the left edge.
3. All the **leaves**, from left to right.
4. The **right edge**, bottom to top: built the same way from the root's right child, preferring right children, leaves excluded.

Every node appears at most once. A tree with a single node has the outline `[root]`.

{{examples}}

**Constraints**
- The tree has between `1` and `10⁴` nodes.
- `-1000 ≤ node value ≤ 1000`
