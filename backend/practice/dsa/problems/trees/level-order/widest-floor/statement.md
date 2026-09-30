Picture each floor of a binary tree as a row of seats that would be completely filled if the tree were perfect: floor `d` has `2ᵈ` seats, and a node's children sit in the two seats directly below it. The **width** of a floor is the number of seats from its leftmost node to its rightmost node, inclusive, counting the empty seats between them.

Return the largest width among all floors.

{{examples}}

**Constraints**
- The tree has between `1` and `10⁵` nodes.
- `-1000 ≤ value ≤ 1000`
- The answer is at most `10¹⁸`.
