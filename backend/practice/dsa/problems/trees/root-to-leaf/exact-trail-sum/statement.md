A hiking map is a binary tree of checkpoints; each checkpoint changes your altitude by its value (possibly negative). A **trail** starts at the root and ends at a leaf (a checkpoint with no children), and its total is the sum of its checkpoints' values.

Return `true` if some trail's total is exactly `target`, otherwise `false`. An empty map has no trails.

{{examples}}

**Constraints**
- The tree has between `0` and `10⁵` nodes.
- `-1000 ≤ value ≤ 1000`
- `-10⁸ ≤ target ≤ 10⁸`
