Row `1` is the single symbol `0`. Each next row is built from the one before by replacing every `0` with `01` and every `1` with `10`. So row 2 is `01`, row 3 is `0110`, row 4 is `01101001`.

Return the `k`-th symbol (1-indexed) of row `n`.

{{examples}}

**Constraints**
- `1 ≤ n ≤ 60`
- `1 ≤ k ≤ 2ⁿ⁻¹`
