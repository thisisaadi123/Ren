A library index stores call numbers in a binary tree that is meant to be a search tree: for every entry, **every** number in its left branch is smaller than it, and **every** number in its right branch is larger.

Return `true` if the whole tree follows this rule and `false` otherwise. Two equal numbers anywhere in the tree break the rule.

{{examples}}

**Constraints**
- The tree has between `1` and `10⁴` nodes.
- `-2³¹ ≤ value ≤ 2³¹ - 1`
