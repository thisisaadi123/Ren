A shop keeps its prices in a binary search tree (for every node, cheaper items on its left side and dearer ones on its right; all prices distinct). The shop now only stocks items priced between `low` and `high`, inclusive.

Remove every node outside that range and return the root of what is left (an empty tree is `[]`). The nodes that stay must keep their relative placement: the parent of a kept node is its **closest ancestor that is also kept**, and it stays on the same side of that ancestor.

{{examples}}

**Constraints**
- The tree has between `1` and `10⁴` nodes and is a valid binary search tree with distinct values.
- `0 ≤ value ≤ 10⁴`
- `0 ≤ low ≤ high ≤ 10⁴`
