`words` is a list of words that all have the same length; a word may appear more than once. A **full chain** is a string made by joining all of `words` together, each exactly as many times as it appears in the list, in any order.

Return every index of `s` where a full chain starts, in increasing order.

{{examples}}

**Constraints**
- `1 ≤ s.length ≤ 10⁴`
- `1 ≤ words.length ≤ 5000`
- `1 ≤ words[i].length ≤ 30`, and all words have the same length.
- `s` and `words[i]` have only lowercase English letters.
