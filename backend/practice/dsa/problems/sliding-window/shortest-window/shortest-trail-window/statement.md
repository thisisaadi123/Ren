A hiker's trail log `s` lists the landmarks passed, one letter each. A guidebook route `t` must be followed in order, but other landmarks may come in between.

Return the **shortest substring** of `s` in which `t` appears as a subsequence: all of `t`'s letters, in order, though not necessarily next to each other. If several shortest substrings exist, return the one that starts **leftmost**. Return `""` if there is none.

{{examples}}

**Constraints**
- `1 ≤ s.length ≤ 2 × 10⁴`
- `1 ≤ t.length ≤ 100`
- `s` and `t` have only lowercase English letters.
