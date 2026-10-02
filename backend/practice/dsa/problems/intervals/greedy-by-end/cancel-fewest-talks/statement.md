A room's schedule `talks` has half-open intervals `[start, end)` that may overlap. Talks that only touch (one ends at `t`, the next starts at `t`) don't overlap.

Return the fewest talks to cancel so that no two remaining talks overlap.

{{examples}}

**Constraints**
- `1 ≤ talks.length ≤ 10⁵`
- `0 ≤ start < end ≤ 10⁹`
