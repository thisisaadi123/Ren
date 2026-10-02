A binary tree with **distinct** values was walked twice: `inorder` (left subtree, then node, then right subtree) and `postorder` (left subtree, then right subtree, then node).

Rebuild the tree and return its root.

{{examples}}

**Constraints**
- `1 ≤ inorder.length == postorder.length ≤ 3 × 10⁴`
- `-10⁵ ≤ value ≤ 10⁵`, all distinct.
- Both lists come from the same tree.
