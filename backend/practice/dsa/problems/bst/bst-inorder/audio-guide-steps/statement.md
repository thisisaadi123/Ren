A museum's exhibit numbers are stored in a binary search tree (for every node, smaller numbers on its left side and larger on its right, all distinct). The audio guide visits the exhibits in increasing order and understands two commands:

- `"next"` moves to the next exhibit and reports its number (the first `"next"` reports the smallest number).
- `"hasNext"` reports `1` if some exhibit hasn't been visited yet, and `0` otherwise.

Run the commands in `ops` in order and return what each one reports. `"next"` is only used while an unvisited exhibit remains.

{{examples}}

**Constraints**
- The tree has between `1` and `10⁵` nodes and is a valid binary search tree with distinct values.
- `-10⁹ ≤ value ≤ 10⁹`
- `1 ≤ ops.length ≤ 2 × 10⁵`, and each `ops[i]` is `"next"` or `"hasNext"`.
- The number of `"next"` commands never exceeds the number of nodes.
