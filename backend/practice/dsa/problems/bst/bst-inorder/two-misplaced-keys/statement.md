A key cabinet is organised as a binary search tree: every key in a node's left branch is smaller than the node's key and every key in its right branch is larger. While cleaning, someone swapped the keys of **exactly two** nodes, and the tree no longer follows the rule.

Swap those two keys back (keep the shape of the tree) and return the root.

{{examples}}

**Constraints**
- The tree has between `2` and `10⁴` nodes, with distinct keys.
- `-2³¹ ≤ key ≤ 2³¹ - 1`
- The tree is exactly one swap of two keys away from a valid search tree, and it is not already valid.
