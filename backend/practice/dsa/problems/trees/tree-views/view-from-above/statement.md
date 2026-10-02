Give every node of the binary tree `root` a **column**: the root is in column `0`, a left child is one column left of its parent, and a right child is one column right.

Looking down from above, you see the **highest** node in each column. If two nodes in the same column are equally high, you see the one that comes first from left to right on that level.

Return the visible values ordered by column, from leftmost to rightmost.

{{examples}}

**Constraints**
- The tree has between `1` and `10⁴` nodes.
- `-10⁴ ≤ node value ≤ 10⁴`
