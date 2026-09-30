A paper strip of labels is stored as a linked list `L0 → L1 → … → L(n−1)`. Folding it in half and reading the layers alternately gives the order

`L0 → L(n−1) → L1 → L(n−2) → L2 → L(n−3) → …`

Rearrange the nodes into that order and return the head. Move the nodes themselves rather than copying values, using O(1) extra memory.

{{examples}}

**Constraints**
- The list has between `0` and `10⁵` nodes.
- `-10⁶ ≤ node value ≤ 10⁶`
