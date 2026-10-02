`meetings` are half-open intervals `[start, end)`. A room can host one meeting at a time, and a meeting that ends at time `t` frees its room for one starting at `t`.

Return the fewest rooms needed to hold every meeting.

{{examples}}

**Constraints**
- `1 ≤ meetings.length ≤ 10⁵`
- `0 ≤ start < end ≤ 10⁹`
