Compress `text` with run-length coding: each run of the same character becomes the character followed by the run's length. A run of length `1` is written as just the character.

For example, `"aaabcc"` becomes `"a3bc2"`. Return the compressed text.

{{examples}}

**Constraints**
- `1 ≤ text.length ≤ 10⁵`
- `text` has lowercase English letters.
