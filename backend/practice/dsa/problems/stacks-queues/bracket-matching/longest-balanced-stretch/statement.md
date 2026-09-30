A signal is recorded as a string of `(` and `)`. A **balanced stretch** is a contiguous piece of the signal in which every `(` is closed by a later `)` inside the piece, and no `)` appears without an open `(` before it in the piece.

Return the length of the longest balanced stretch, or `0` if there is none.

{{examples}}

**Constraints**
- `1 ≤ s.length ≤ 10⁵`
- `s` contains only `(` and `)`.
