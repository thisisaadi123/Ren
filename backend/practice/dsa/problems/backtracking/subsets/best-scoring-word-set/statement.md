In a tile game you hold a bag of letter tiles, given as the string `tiles` (a letter can appear several times). You may spell any set of words from the list `words`, each entry at most once. Spelling a word uses up one tile for each of its letters, and a tile can't be reused.

Every tile of letter `c` is worth `points[c - 'a']`, and a word scores the total of its letters. Return the highest total score you can reach with one set of words (spelling nothing scores `0`).

{{examples}}

**Constraints**
- `1 ≤ words.length ≤ 14`
- `1 ≤ words[i].length ≤ 15`
- `1 ≤ tiles.length ≤ 100`
- `points.length == 26`
- `0 ≤ points[i] ≤ 10`
- `words[i]` and `tiles` contain only lowercase English letters.
