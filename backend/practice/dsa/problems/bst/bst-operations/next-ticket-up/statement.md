A deli hands out numbered tickets, and the numbers still waiting are stored in a binary search tree (smaller numbers on the left of a node, larger on the right, all distinct).

Given a number `x`, return the smallest waiting ticket number that is **strictly greater** than `x`, or `-1` if there is none. `x` itself may or may not be in the tree.

{{examples}}

**Constraints**
- The tree has between `0` and `10⁴` nodes and is a valid binary search tree with distinct values.
- `0 ≤ value ≤ 10⁹`
- `0 ≤ x ≤ 10⁹`
