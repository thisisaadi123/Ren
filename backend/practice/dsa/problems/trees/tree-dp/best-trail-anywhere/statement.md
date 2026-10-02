A hiking map is a binary tree `root`, and each node's value is the scenery score of that spot, which can be negative. A **trail** is any path between two nodes along the tree's edges, visiting each node at most once; it must contain at least one node, and doesn't have to pass through the root.

Return the largest total score of any trail.

{{examples}}

**Constraints**
- The tree has between `1` and `3 × 10⁴` nodes.
- `-1000 ≤ node value ≤ 1000`
