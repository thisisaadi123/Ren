A config file wraps its sections in three kinds of brackets: `()`, `[]` and `{}`. The file is **sealed** when every opening bracket is closed by a bracket of the same kind, and the most recently opened bracket is always the first one closed.

Return `true` if `s` is sealed, otherwise `false`.

{{examples}}

**Constraints**
- `1 ≤ s.length ≤ 10⁵`
- `s` contains only the characters `()[]{}`.
