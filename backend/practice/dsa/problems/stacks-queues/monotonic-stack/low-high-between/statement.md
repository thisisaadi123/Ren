A chart lists `values` in time order. Look for three moments `i < j < k` where the first is the lowest, the second is the highest, and the third lands strictly **in between**: `values[i] < values[k] < values[j]`.

Return `true` if such three moments exist, otherwise `false`.

{{examples}}

**Constraints**
- `1 ≤ values.length ≤ 10⁵`
- `-10⁹ ≤ values[i] ≤ 10⁹`
