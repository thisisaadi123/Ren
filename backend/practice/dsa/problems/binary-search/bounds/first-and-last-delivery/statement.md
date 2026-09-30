`times` lists delivery timestamps in non-decreasing order; several deliveries can share a timestamp. For the timestamp `target`, return `[first, last]`: the first and last positions where it appears. If it doesn't appear, return `[-1, -1]`.

Your solution must run in O(log n) time.

{{examples}}

**Constraints**
- `0 ≤ times.length ≤ 10⁵`
- `-10⁹ ≤ times[i], target ≤ 10⁹`
- `times` is sorted in non-decreasing order.
