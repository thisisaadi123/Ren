`prices` is sorted in non-decreasing order. Return the `k` prices closest to `x`, in increasing order.

A price `a` is closer than `b` if `|a - x| < |b - x|`, or if they're equally close and `a < b`.

{{examples}}

**Constraints**
- `1 ≤ k ≤ prices.length ≤ 10⁵`
- `-10⁹ ≤ prices[i], x ≤ 10⁹`
- `prices` is sorted in non-decreasing order.
