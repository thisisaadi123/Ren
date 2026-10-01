A car's odometer is stored as a linked list of digits, **most significant digit first**: `1 → 2 → 9` means 129. The number has no leading zeros, except for the number 0 itself.

The car drives one more mile. Return the list for the reading plus one.

{{examples}}

**Constraints**
- The list has `n` nodes, `1 ≤ n ≤ 10⁵`.
- `0 ≤ node value ≤ 9`
- The first node is `0` only when the list is just `[0]`.
