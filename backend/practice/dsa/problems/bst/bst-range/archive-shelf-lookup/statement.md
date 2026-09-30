An archive stores document ids in a binary search tree (for every node, smaller ids on its left side and larger ones on its right; all ids distinct). Clerks ask many questions of the form `[low, high, k]`: among the ids between `low` and `high` inclusive, which is the `k`-th smallest?

Return an array with one answer per query: that id, or `-1` if fewer than `k` ids lie in the band.

{{examples}}

**Constraints**
- The tree has between `1` and `10⁵` nodes and is a valid binary search tree with distinct values.
- `0 ≤ value ≤ 10⁹`
- `1 ≤ queries.length ≤ 10⁵`
- `queries[i] = [low, high, k]` with `0 ≤ low ≤ high ≤ 10⁹` and `1 ≤ k ≤ 10⁵`
