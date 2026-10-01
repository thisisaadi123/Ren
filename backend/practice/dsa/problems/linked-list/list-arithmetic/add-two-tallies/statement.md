Two clerks keep tallies as linked lists of digits stored **ones digit first**: `3 → 4 → 2` is 243. Neither tally has leading zeros, except the tally 0 itself, which is `[0]`.

Return the sum of the two tallies as a list in the same form.

{{examples}}

**Constraints**
- Each list has between `1` and `10⁵` nodes.
- `0 ≤ node value ≤ 9`
- The last node of a list is `0` only when the list is just `[0]`.
