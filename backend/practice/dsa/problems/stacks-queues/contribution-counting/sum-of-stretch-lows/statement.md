`prices` is a stock's price over consecutive days. Every non-empty stretch of consecutive days has a **low**, its smallest price.

Return the sum of the lows of all stretches. The answer can be huge, so return it modulo `10⁹ + 7`.

{{examples}}

**Constraints**
- `1 ≤ prices.length ≤ 10⁵`
- `1 ≤ prices[i] ≤ 3 × 10⁴`
