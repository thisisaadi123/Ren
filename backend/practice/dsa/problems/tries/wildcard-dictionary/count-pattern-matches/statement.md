For each pattern in `patterns`, count how many entries of `words` match it. A word matches when it has the same length as the pattern and every letter of the pattern equals the word's letter at that position; a `.` in the pattern matches any letter. Repeated words count each time.

{{examples}}

**Constraints**
- `1 ≤ words.length ≤ 5000`, `1 ≤ patterns.length ≤ 5000`
- `1 ≤ words[i].length, patterns[j].length ≤ 10`
- Words are lowercase; patterns are lowercase with at most `2` dots.
