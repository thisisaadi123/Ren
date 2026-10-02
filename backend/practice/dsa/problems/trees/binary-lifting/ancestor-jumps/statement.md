A family tree has `n` people numbered `0` to `n − 1`. `parent[i]` is person `i`'s parent; person `0` is the root, with `parent[0] = -1`.

Each query `[v, k]` asks for person `v`'s **`k`-th ancestor**: their parent is the 1st, their grandparent the 2nd, and so on. Return the answer to every query in order, using `-1` when the ancestor doesn't exist.

{{examples}}

**Constraints**
- `1 ≤ n ≤ 5 × 10⁴`
- `parent[0] = -1`, and the parent links form a single tree rooted at `0`.
- `1 ≤ queries.length ≤ 5 × 10⁴`
- `0 ≤ v < n`, `1 ≤ k ≤ n`
