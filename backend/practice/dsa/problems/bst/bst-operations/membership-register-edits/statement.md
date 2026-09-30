A club stores member numbers in a binary search tree (for every node, smaller numbers on its left side, larger on its right, all distinct). You are given the tree and a list of edits `ops`, applied in order:

- `[1, k]` **inserts** `k`: walk down from the root as if searching for `k` and attach it as a new leaf where the search falls off. If `k` is already there, nothing happens.
- `[0, k]` **deletes** `k` if it is there (otherwise nothing happens):
  - a node with no children is removed;
  - a node with one child is replaced by that child (the child keeps its whole side);
  - a node with two children takes the key of the **smallest** node on its right side, and that smallest node is then removed by the rule above.

Return the root of the tree after all edits (an empty tree is `[]`).

{{examples}}

**Constraints**
- The starting tree has between `0` and `1000` nodes and is a valid binary search tree with distinct values.
- `1 ≤ ops.length ≤ 1000`
- Each `ops[i]` is `[0, k]` or `[1, k]` with `-10⁵ ≤ k ≤ 10⁵`.
- `-10⁵ ≤ value ≤ 10⁵`
