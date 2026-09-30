You can change a word with two kinds of moves, as many times as you like and in any order:

- **Swap:** exchange the positions of any two letters.
- **Relabel:** pick two different letters that **both** appear in the word, and turn every copy of the first into the second and every copy of the second into the first.

For example, `"aab"` can become `"bba"` with one relabel. Return `true` if word `a` can be turned into word `b`.

{{examples}}

**Constraints**
- `1 ≤ a.length, b.length ≤ 10⁵`
- `a` and `b` have only lowercase English letters.
