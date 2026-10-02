A cave system is a binary tree `root` with distinct values, and its **exits** are the leaves (nodes with no children). From the node with value `start`, moving to a parent or a child takes one step.

Return the value of the exit with the fewest steps from `start`. If several exits tie, return the smallest value. If `start` is itself a leaf, return `start`.

{{examples}}

**Constraints**
- The tree has between `1` and `10⁴` nodes.
- `0 ≤ node value ≤ 10⁵`, all distinct.
- `start` is in the tree.
