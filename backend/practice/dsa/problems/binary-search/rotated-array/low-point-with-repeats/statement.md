A log of readings was non-decreasing (readings can repeat) and was then rotated. Return the smallest reading.

Aim for O(log n) on average; with many repeats the worst case is O(n).

{{examples}}

**Constraints**
- `1 ≤ readings.length ≤ 10⁵`
- `-5000 ≤ readings[i] ≤ 5000`
- `readings` is a rotation of a non-decreasing list.
