A charity's regional offices form a binary tree; each office has a distinct ID and starts with a tally of `0`. You process `ops` in order:
- `[1, v, x]`: office `v` receives `x` more in donations.
- `[2, v]`: report the total tally of office `v` and every office in its branch (its whole subtree).

Return the reported totals in the order the reports happen.

{{examples}}

**Constraints**
- The tree has between `1` and `10⁵` offices, with distinct IDs.
- `1 ≤ ID ≤ 10⁶`
- `1 ≤ ops.length ≤ 10⁵`
- Each op is `[1, v, x]` with `1 ≤ x ≤ 10⁹`, or `[2, v]`; `v` is always in the tree.
