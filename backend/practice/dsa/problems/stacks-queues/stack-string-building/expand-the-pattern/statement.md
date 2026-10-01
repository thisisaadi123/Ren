A knitting pattern compresses repeats as `k[...]`: the part inside the brackets is written out `k` times. Groups can be nested, as in `2[a3[b]]`.

Return the fully expanded pattern.

{{examples}}

**Constraints**
- `1 ≤ pattern.length ≤ 3000`
- `pattern` is well formed: lowercase letters, digits and square brackets, where every `[` comes right after a whole number `k` with `1 ≤ k ≤ 300`, and every number is followed by `[`.
- The expanded pattern has at most `10⁵` characters.
