`slots` is a sorted list of non-overlapping **half-open** intervals `[start, end)`: each contains `start` but not `end`. Remove the half-open range `cut = [a, b)` from them.

Return what's left, as sorted half-open intervals. Pieces of zero length are dropped.

{{examples}}

**Constraints**
- `1 ≤ slots.length ≤ 10⁵`
- `0 ≤ start < end ≤ 10⁹`, sorted, and an interval may start where the previous one ends.
- `cut = [a, b)` with `0 ≤ a < b ≤ 10⁹`
