Place every node of a binary tree on a grid: the root is at row `0`, column `0`; a node's left child is one row down and one column left, and its right child one row down and one column right.

Read the tree **column by column**, from the leftmost column to the rightmost. Within a column, list nodes from top to bottom; nodes in the **same row and column** are listed from smallest value to largest.

Return one list per column.

{{examples}}

**Constraints**
- The tree has between `1` and `10⁴` nodes.
- `0 ≤ node value ≤ 1000`
