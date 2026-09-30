Shifting a word moves every letter forward by the same number of places in the alphabet, wrapping from `z` back to `a`. For example, shifting `"abc"` by 1 gives `"bcd"`, and shifting `"az"` by 1 gives `"ba"`.

Words that can be shifted into each other form a **family**. Return how many families the `words` fall into. Identical words are in the same family.

{{examples}}

**Constraints**
- `1 ≤ words.length ≤ 10⁴`
- `1 ≤ words[i].length ≤ 50`
- Words contain only lowercase English letters.
