A hall's `bookings` are closed intervals `[start, end]`. Two bookings that overlap or **touch** (one ends exactly when the other starts) are combined into one.

Return the combined bookings, sorted by start.

{{examples}}

**Constraints**
- `1 ≤ bookings.length ≤ 10⁵`
- `0 ≤ start ≤ end ≤ 10⁹`
