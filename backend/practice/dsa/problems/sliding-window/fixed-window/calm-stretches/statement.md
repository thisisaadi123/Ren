A sensor logs the noise level every minute in `noise`. A stretch of exactly `k` consecutive minutes is **calm** when its average noise level is **at most** `limit`.

Return how many calm stretches there are.

{{examples}}

**Constraints**
- `1 ≤ k ≤ noise.length ≤ 10⁵`
- `0 ≤ noise[i] ≤ 10⁴`
- `0 ≤ limit ≤ 10⁴`
