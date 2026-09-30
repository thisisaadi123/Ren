A shipping label describes nested gift boxes as a balanced string of brackets. Its value follows three rules:
- An empty box `()` is worth `1`.
- Boxes side by side, `AB`, are worth the value of `A` plus the value of `B`.
- A box wrapped around non-empty contents, `(A)`, is worth `2 ×` the value of `A`.

Return the value of `s`, modulo `10⁹ + 7`.

{{examples}}

**Constraints**
- `2 ≤ s.length ≤ 10⁵`
- `s` contains only `(` and `)`, and it is balanced.
