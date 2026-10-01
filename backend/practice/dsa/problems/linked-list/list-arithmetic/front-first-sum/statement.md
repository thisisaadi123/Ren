Two meters print their readings as linked lists of digits, **most significant digit first**: `7 → 2 → 4 → 3` is 7243. Neither reading has leading zeros, except the reading 0 itself, which is `[0]`.

Return the combined reading, the sum of the two, as a list in the same front-first form.

{{examples}}

**Constraints**
- Each list has between `1` and `10⁵` nodes.
- `0 ≤ node value ≤ 9`
- The first node of a list is `0` only when the list is just `[0]`.
