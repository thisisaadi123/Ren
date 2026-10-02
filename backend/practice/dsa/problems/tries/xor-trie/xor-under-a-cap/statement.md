Each query `[x, m]` asks for the largest value of `x XOR nums[j]` over all `nums[j] ≤ m`. If no number is at most `m`, the answer is `-1`.

Return the answers in the order of `queries`.

{{examples}}

**Constraints**
- `1 ≤ nums.length, queries.length ≤ 2 × 10⁴`
- `0 ≤ nums[j], x, m ≤ 10⁹`
