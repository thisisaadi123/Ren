A leaderboard keeps `scores` sorted in increasing order, all different. If `target` is already on the board, return its position. Otherwise return the position where it would be inserted to keep the board sorted.

Your solution must run in O(log n) time.

{{examples}}

**Constraints**
- `1 ≤ scores.length ≤ 10⁵`
- `-10⁹ ≤ scores[i], target ≤ 10⁹`
- `scores` is strictly increasing.
