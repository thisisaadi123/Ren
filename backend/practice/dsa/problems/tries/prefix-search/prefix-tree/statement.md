Implement a **prefix tree** that stores words:

- `PrefixTree()` starts empty.
- `insert(word)` stores `word`.
- `search(word)` returns `true` if `word` itself was stored.
- `startsWith(prefix)` returns `true` if some stored word starts with `prefix`.

{{examples}}

**Constraints**
- `1 ≤ word.length, prefix.length ≤ 50`
- Words and prefixes have only lowercase English letters.
- At most `3 × 10⁴` calls in total.
