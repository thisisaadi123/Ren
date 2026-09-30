# Progress tracking

> **Storage isn't chosen yet.** The dev server (`server.js`) keeps accounts in memory only, so nothing here can be saved until a database is picked (e.g. SQLite for development, Postgres in production). This file defines *what* we record and *how* it rolls up.

## Per user and problem
| Field | Meaning |
|---|---|
| `user_id`, `problem_id` | Who, and which problem (`problem.yaml` `id`) |
| `status` | `not_started` → `tried` → `solved` |
| `help_level` | The highest Ren step used on the problem: `none`, `hint`, `nudge`, `explain` or `solve` |
| `solved_version` | The problem `version` the passing submission was checked against |
| `attempts` | The number of Submits |
| `first_solved_at`, `last_activity_at` | Timestamps |
| `time_spent_s` | Active time on the problem page |
| `language` | The language of the accepted submission |

A problem is **solved on your own** when `status = solved` and `help_level` isn't `solve`. The Hint, Nudge and Explain steps still count as your own solve, because they teach the pattern without giving away the code.

## Rollups
- **Pattern progress:** problems solved out of the pattern's count. Shown as a plain progress bar.
- **Pattern mastered** when:
  - the pattern's Easy problems are solved on your own, **and**
  - at least one Medium problem in the pattern is solved on your own (or a Hard one, if the pattern has no Medium).
- **Topic progress:** problems solved out of the topic's count, plus mastered patterns out of all its patterns.
- **Topic complete** when every pattern in it is mastered. That's what unlocks the topic's LeetCode sheet (see `sheets.md`).
- **Weakest pattern:** the started-but-not-mastered pattern with the lowest progress, or the next pattern in order if nothing is started. Ren uses it to suggest what to do next.

## What Ren suggests next
1. Keep going in the current pattern until it's mastered.
2. Then suggest the next unmastered pattern in the same topic.
3. When the topic is complete, suggest the next topic whose `prerequisites` are all complete, in track order. Prerequisites are suggestions, not locks: any topic can be opened at any time.

## LeetCode sheet progress
Kept **separate** from verified progress. Ren can't see LeetCode submissions (there's no official API), so users tick sheet problems off themselves. Store `user_id`, `sheet_topic`, `leetcode_slug` and `checked_at`. Sheet ticks never count toward mastery.

## UI rules for later
- Plain progress bars and text ("4 of 8 solved").
- No pills, badges or chips. That's a Ren style rule.
