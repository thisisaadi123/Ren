Two calendars `a` and `b` list events as half-open intervals `[start, end)`, each sorted and non-overlapping. Return `true` if some event in `a` overlaps some event in `b`. Events that only touch (one ends at `t`, the other starts at `t`) don't clash.

{{examples}}

**Constraints**
- `1 ≤ a.length, b.length ≤ 10⁵`
- `0 ≤ start < end ≤ 10⁹`; within each calendar, events don't overlap.
