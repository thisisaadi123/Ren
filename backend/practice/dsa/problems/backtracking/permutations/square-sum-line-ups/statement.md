You are lining up number cards whose values are in `nums`. A line-up uses every card exactly once, and it is **square-linked** if every two neighbouring cards add up to a perfect square (`0`, `1`, `4`, `9`, ...).

Cards with the same value are interchangeable, so two line-ups are the same if they read the same value by value. Return the number of different square-linked line-ups. A single card on its own is a valid line-up.

{{examples}}

**Constraints**
- `1 ≤ nums.length ≤ 12`
- `0 ≤ nums[i] ≤ 10⁹`
