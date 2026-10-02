A worker's `shifts` are intervals `[start, end]`. A break of at most `gap` minutes between two shifts is too short to go home, so such shifts count as one **block** (overlapping shifts are in one block too).

Return the blocks, sorted by start.

{{examples}}

**Constraints**
- `1 ≤ shifts.length ≤ 10⁵`
- `0 ≤ start ≤ end ≤ 10⁹`
- `0 ≤ gap ≤ 10⁹`
