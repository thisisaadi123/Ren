Group the `words` so that words that are anagrams of each other (the same letters, rearranged) end up in the same group.

So that there's one right answer: sort the words inside each group alphabetically, then order the groups alphabetically by their first word. Keep duplicates.

{{examples}}

**Constraints**
- `1 ≤ words.length ≤ 10⁴`
- `0 ≤ words[i].length ≤ 30`
- Words contain only lowercase English letters.
