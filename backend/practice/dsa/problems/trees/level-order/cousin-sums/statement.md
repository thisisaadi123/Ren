In a family tree, two people are **cousins** when they are on the same floor (same depth) but have different parents. Replace every person's value with the **sum of their cousins' values** (the original values), or `0` if they have no cousins. The root and the root's children never have cousins.

Return the root of the same tree with the new values.

{{examples}}

**Constraints**
- The tree has between `1` and `10⁵` nodes.
- `1 ≤ value ≤ 10⁴`
