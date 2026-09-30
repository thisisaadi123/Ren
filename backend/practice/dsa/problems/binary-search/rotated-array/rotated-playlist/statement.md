A playlist's track ids were sorted in increasing order (all different), then the playlist was rotated: some prefix was moved to the end. For example `[1, 3, 5, 7, 9]` might become `[7, 9, 1, 3, 5]`.

Return the position of `target`, or `-1` if it isn't in the playlist. Your solution must run in O(log n) time.

{{examples}}

**Constraints**
- `1 ≤ playlist.length ≤ 10⁵`
- `-10⁹ ≤ playlist[i], target ≤ 10⁹`
- The values are distinct, and `playlist` is a rotation of a sorted list.
