`bookings` is a list of closed intervals `[start, end]`, sorted by start, with no two overlapping or touching. Add the booking `extra`, combining it with every booking it overlaps or touches.

Return the new list, still sorted and non-overlapping.

{{examples}}

**Constraints**
- `0 ≤ bookings.length ≤ 10⁵`
- `0 ≤ start ≤ end ≤ 10⁹`; `extra = [start, end]` follows the same rule.
