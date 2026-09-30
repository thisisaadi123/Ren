A **chain** with step `step` is a list of numbers where each one is exactly `step` more than the one before it, such as `4, 7, 10` for `step = 3`.

Using the numbers in `values` (in any order, each at most once), return the length of the longest chain you can build.

{{examples}}

**Constraints**
- `1 ≤ values.length ≤ 10⁵`
- `-10⁹ ≤ values[i] ≤ 10⁹`
- `1 ≤ step ≤ 10⁹`
