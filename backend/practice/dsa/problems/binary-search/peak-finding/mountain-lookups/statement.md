`elevations` is a mountain: it rises strictly to one top and then falls strictly, and the top isn't at either end.

For each value in `targets`, return the **smallest** index `i` with `elevations[i] == target`, or `-1` if no point has that elevation. Answer in the order of `targets`.

With up to `10⁵` lookups, checking every point for every lookup is too slow.

{{examples}}

**Constraints**
- `3 ≤ elevations.length ≤ 10⁵`
- `1 ≤ targets.length ≤ 10⁵`
- `0 ≤ elevations[i], targets[j] ≤ 10⁹`
