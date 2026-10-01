A candy game drops tiles in a row, written as the string `s`. Whenever **`k` identical tiles** sit next to each other, they're crushed and removed, and the tiles on either side slide together. Crushing repeats until no `k` identical neighbours remain.

Return the final row. The result is the same whatever order the crushes happen in.

{{examples}}

**Constraints**
- `1 ≤ s.length ≤ 10⁵`
- `2 ≤ k ≤ 10⁴`
- `s` has only lowercase English letters.
