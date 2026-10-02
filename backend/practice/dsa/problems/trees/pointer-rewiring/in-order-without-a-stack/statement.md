Return the in-order walk (left subtree, node, right subtree) of the binary tree `root`.

This would be easy with recursion or a stack. Try to use only **O(1) extra memory** by temporarily rewiring the tree's own empty right pointers, and put the tree back the way you found it before you return.

{{examples}}

**Constraints**
- The tree has between `0` and `3 × 10⁴` nodes.
- `-1000 ≤ node value ≤ 1000`
