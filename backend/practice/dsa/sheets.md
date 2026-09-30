# LeetCode sheets

When a user **completes a topic** (every pattern in it mastered; see `progress.md`), they unlock that topic's **sheet**: our hand-picked list of the important LeetCode problems for the topic, as links out to LeetCode.

Until then, the topic page shows the sheet locked, with what's left in plain text and a progress bar, e.g. "Master 3 more patterns to unlock the Binary Search sheet".

## What's in a sheet
- **About 25–40 problems per topic,** grouped under **the same patterns as `taxonomy.yaml`** and ordered Easy → Hard within each pattern.
- Each entry shows:
  - the problem's title, linked to its LeetCode page (opens in a new tab)
  - its difficulty and pattern
  - a one-line note **in our own words** on why it matters (e.g. "The classic search-on-the-answer setup: learn the feasibility check here")
  - a link to the **Ren sibling problem**, the Ren problem that trains the same pattern
- Problems that need LeetCode Premium get a plain "Premium on LeetCode" note, not a badge. Prefer free problems. At most 20% of a sheet may be Premium.

## Copyright rules
- **We store and show only the title and the link.** Never LeetCode's problem text, examples, constraints, test cases, editorials or logo.
- The choice, grouping and notes are our own work.
- Plain text only. Nothing may suggest Ren is affiliated with LeetCode.

## Test cases
Sheet problems are solved **on LeetCode**, so their tests run there. We don't copy LeetCode's tests. Anyone who wants to practice the same pattern inside Ren, with tests and hints, uses the sibling problem.

## File format: `sheets/<topic-id>.yaml`
```yaml
topic: binary-search          # a topic id from taxonomy.yaml
version: 1
entries:
  - slug: some-problem-slug   # the part after leetcode.com/problems/
    title: Some Problem Title  # the title as shown on LeetCode
    difficulty: medium         # easy | medium | hard, as LeetCode labels it
    pattern: search-on-answer  # a pattern id from this topic in taxonomy.yaml
    premium: false
    note: One line in our own words.
    ren_problem: print-shop-daily-limit   # optional: a Ren problem id with the same pattern
```

The link is always built as `https://leetcode.com/problems/<slug>/`. It's never stored, so a URL change is a one-line fix.

## Checks
- **In CI:**
  - the file parses
  - `topic` exists, and every `pattern` belongs to that topic
  - no duplicate slugs within a sheet
  - `ren_problem` (when set) exists and has the same pattern
  - no more than 20% `premium: true`
  - every `note` is filled in
- **Weekly, not in CI:** a link check that each slug still resolves. It's not in CI because LeetCode may block automated requests; a failed check opens an issue instead.

## When sheets are written
Alongside each topic's problem batch. The Binary Search sheet ships with the pilot. `sheets/_example.yaml` shows the format only. It isn't a real sheet, and the app ignores any file starting with `_`.
