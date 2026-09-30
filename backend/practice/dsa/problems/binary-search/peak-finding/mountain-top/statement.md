A trail rises strictly to a single top and then falls strictly: `elevations[0] < … < elevations[top] > … > elevations[n - 1]`, and the top is never the first or last point.

Return the index of the top in O(log n) time.

{{examples}}

**Constraints**
- `3 ≤ elevations.length ≤ 10⁵`
- `0 ≤ elevations[i] ≤ 10⁹`
- `elevations` is a mountain as described above.
