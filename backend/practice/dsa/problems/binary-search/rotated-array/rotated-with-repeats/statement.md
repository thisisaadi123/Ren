A shelf of book ids was sorted in non-decreasing order (ids can repeat) and then rotated. Return `true` if `target` is on the shelf.

Aim for O(log n) on average; with many repeats, O(n) is unavoidable in the worst case.

{{examples}}

**Constraints**
- `1 ≤ shelf.length ≤ 10⁵`
- `-10⁴ ≤ shelf[i], target ≤ 10⁴`
- `shelf` is a rotation of a non-decreasing list.
