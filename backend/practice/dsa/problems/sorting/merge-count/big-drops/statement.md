`prices` is a stock's price history. A **big drop** is a pair of days `i < j` where the earlier price is **more than double** the later one: `prices[i] > 2 · prices[j]`.

Return the number of big drops.

{{examples}}

**Constraints**
- `1 ≤ prices.length ≤ 5 × 10⁴`
- `-2³¹ ≤ prices[i] ≤ 2³¹ - 1`
