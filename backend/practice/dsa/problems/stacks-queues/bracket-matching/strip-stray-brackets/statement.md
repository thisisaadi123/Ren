A note mixes lowercase words with brackets, and some brackets are stray: they have no partner. Remove the **fewest** brackets so that the brackets left over are balanced (each `(` is closed by a later `)`, and no `)` appears without an open `(` before it). Letters are never removed.

Return the cleaned string. If several answers remove the same, smallest number of brackets, return any of them.

{{examples}}

**Constraints**
- `1 ≤ s.length ≤ 10⁵`
- `s` contains only lowercase English letters, `(` and `)`.
