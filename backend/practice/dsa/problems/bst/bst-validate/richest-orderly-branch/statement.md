A binary tree holds a number in every node, positive or negative. A **branch** is a node together with all of its descendants. A branch is **orderly** if it is a strict binary search tree: for every node in it, every value in its left side is smaller and every value in its right side is larger.

Return the largest total of values over all orderly branches. A single leaf is always an orderly branch, so an answer always exists, and it may be negative.

{{examples}}

**Constraints**
- The tree has between `1` and `4 × 10⁴` nodes.
- `-4 × 10⁴ ≤ value ≤ 4 × 10⁴`
