You want to buy exactly two different gifts and spend your whole `budget`. `prices[i]` is the price of gift `i`.

Exactly one pair of gifts adds up to `budget`. Return their indices `[i, j]` with `i < j`.

{{examples}}

**Constraints**
- `2 ≤ prices.length ≤ 10⁵`
- `-10⁹ ≤ prices[i] ≤ 10⁹` (negative prices are coupons)
- `-2 × 10⁹ ≤ budget ≤ 2 × 10⁹`
- Exactly one pair `i < j` has `prices[i] + prices[j] == budget`.
