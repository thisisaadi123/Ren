A hiking trail's heights are listed in `heights`, and neighbouring points are never equal. A **summit** is a point strictly higher than its neighbours; pretend there's a bottomless drop before the first point and after the last one.

Return the index of **any** summit. Your solution must run in O(log n) time.

{{examples}}

**Constraints**
- `1 ≤ heights.length ≤ 10⁵`
- `-2³¹ ≤ heights[i] ≤ 2³¹ - 1`
- `heights[i] != heights[i + 1]`
