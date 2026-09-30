A library keeps its catalogue as a binary tree of shelf codes. The clerk reads the codes aloud in **shelf order**: for every node, first everything in its left branch (in shelf order), then the node itself, then everything in its right branch (in shelf order).

Return the codes in the order the clerk reads them. An empty catalogue gives an empty list.

{{examples}}

**Constraints**
- The tree has between `0` and `10⁵` nodes.
- `-1000 ≤ value ≤ 1000`
