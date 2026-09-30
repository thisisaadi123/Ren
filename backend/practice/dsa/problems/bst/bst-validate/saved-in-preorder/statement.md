A binary search tree with distinct keys was saved to disk by writing its keys in **preorder**: a node's key, then its whole left side, then its whole right side. In a binary search tree every key on a node's left side is smaller than the node's key and every key on its right side is larger.

Given the saved sequence `keys`, return `true` if it could be the preorder of some binary search tree, and `false` if the file must be corrupted.

{{examples}}

**Constraints**
- `1 ≤ keys.length ≤ 10⁵`
- `-10⁹ ≤ keys[i] ≤ 10⁹`
- All keys are distinct.
