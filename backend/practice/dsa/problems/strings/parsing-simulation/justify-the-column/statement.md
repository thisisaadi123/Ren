A newspaper column is exactly `width` characters wide. Place the `words` in order, line by line: each line takes as many of the next words as fit with a single space between neighbours.

Then pad every line to exactly `width` characters:
- On a line that isn't the last and has at least two words, spread the spaces over the gaps between words as evenly as possible. If they don't divide evenly, gaps nearer the left get one more space than gaps nearer the right.
- The last line, and any line holding a single word, is left-aligned: one space between words, and the rest of the spaces at the end.

Return the lines from top to bottom.

{{examples}}

**Constraints**
- `1 ≤ words.length ≤ 300`
- `1 ≤ words[i].length ≤ width ≤ 100`
- Words have English letters, digits and the punctuation marks `. , ! ? ' -`, and no spaces.
