Implement a dictionary that supports wildcard lookups:

- `WildcardDictionary()` starts empty.
- `addWord(word)` stores `word`.
- `search(pattern)` returns `true` if some stored word matches `pattern`, where each `.` matches any **one** letter and every other letter must match exactly. The word must have the same length as the pattern.

{{examples}}

**Constraints**
- `1 ≤ word.length, pattern.length ≤ 25`
- Words have only lowercase letters; patterns have lowercase letters and at most `3` dots.
- At most `10⁴` calls in total.
