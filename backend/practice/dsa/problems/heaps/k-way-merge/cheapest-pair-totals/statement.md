A shop sells a main from menu `a` and a side from menu `b`, both sorted in non-decreasing order of price. Every main can pair with every side. Return the `k` cheapest combo prices, cheapest first (equal prices appear as many times as they occur).

{{examples}}

**Constraints**
- `1 ≤ a.length, b.length ≤ 10⁵`
- `1 ≤ k ≤ min(a.length × b.length, 10⁴)`
- `-10⁹ ≤ a[i], b[j] ≤ 10⁹`, both sorted.
