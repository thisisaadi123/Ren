A family tree is a binary tree whose people have distinct ID numbers. For each query `[a, b]`, decide whether person `a` is a **strict ancestor** of person `b`: `a` lies on the path from the root down to `b`, and `a ≠ b`.

Return one `true`/`false` per query, in query order.

{{examples}}

**Constraints**
- The tree has between `1` and `10⁵` people, with distinct IDs.
- `1 ≤ ID ≤ 10⁶`
- `1 ≤ queries.length ≤ 10⁵`
- Both IDs of every query are in the tree.
