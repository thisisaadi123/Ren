A squirrel runs down a binary tree `root`. A **zigzag walk** starts at any node, picks a direction (left or right), moves to that child, then keeps switching direction at every step: left, right, left… or right, left, right… It stops when the next child doesn't exist.

Return the length of the longest zigzag walk, counted in **edges** (a single node is length `0`).

{{examples}}

**Constraints**
- The tree has between `1` and `3 × 10⁴` nodes.
- `1 ≤ node value ≤ 100`
