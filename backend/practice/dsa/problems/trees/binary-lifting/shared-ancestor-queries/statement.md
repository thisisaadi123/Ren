A family tree has `n` people numbered `0` to `n − 1`; `parent[i]` is person `i`'s parent, and person `0` is the root with `parent[0] = -1`.

For each query `[u, v]`, return their **closest shared ancestor**: the deepest person who is an ancestor of both. A person counts as their own ancestor.

{{examples}}

**Constraints**
- `1 ≤ n ≤ 5 × 10⁴`
- `parent[0] = -1`, and the parent links form a single tree rooted at `0`.
- `1 ≤ queries.length ≤ 5 × 10⁴`
- `0 ≤ u, v < n`
