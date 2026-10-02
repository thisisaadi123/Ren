A virus starts at the node with value `start` of a binary tree `root` (values are distinct) at minute `0`. Every minute, each infected node infects its parent and its children.

Return how many minutes it takes for the whole tree to be infected.

{{examples}}

**Constraints**
- The tree has between `1` and `10⁴` nodes.
- `0 ≤ node value ≤ 10⁵`, all distinct.
- `start` is in the tree.
