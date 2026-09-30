A songwriter describes the rhythm of a line with a `pattern` of letters, such as `"abba"`. A `sentence` **follows** the pattern when it has exactly one word per letter and letters and words match one-to-one: the same letter always stands for the same word, and different letters always stand for different words.

For example, `"sun moon moon sun"` follows `"abba"`, but `"sun sun sun sun"` doesn't. Return `true` if `sentence` follows `pattern`.

{{examples}}

**Constraints**
- `1 ≤ pattern.length ≤ 300`
- `1 ≤ sentence.length ≤ 3000`
- `pattern` has only lowercase English letters.
- `sentence` is lowercase English words separated by single spaces, with no leading or trailing spaces.
