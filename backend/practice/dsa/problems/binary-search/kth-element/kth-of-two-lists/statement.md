Given two sorted lists `a` and `b`, return the `k`-th smallest value among all of their values together (`k = 1` is the smallest; duplicates count separately).

Aim for O(log(m + n)) time.

{{examples}}

**Constraints**
- `0 ≤ a.length, b.length ≤ 10⁵`
- `1 ≤ k ≤ a.length + b.length`
- `-10⁹ ≤ a[i], b[i] ≤ 10⁹`, both lists sorted in non-decreasing order
