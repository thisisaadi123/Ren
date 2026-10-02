A binary tree with **distinct** values was walked twice: `preorder` (node, then left subtree, then right subtree) and `inorder` (left subtree, then node, then right subtree).

Rebuild the tree and return its root.

{{examples}}

**Constraints**
- `1 ≤ preorder.length == inorder.length ≤ 3 × 10⁴`
- `-10⁵ ≤ value ≤ 10⁵`, all distinct.
- Both lists come from the same tree.
