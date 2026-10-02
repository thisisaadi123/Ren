A gold mine is a grid `mine` where each cell holds some gold (`0` means empty). A miner may start at any cell with gold, then repeatedly step up, down, left or right to another cell with gold, collecting it. A cell can be visited at most once, and the miner can never step onto an empty cell.

Return the most gold the miner can collect.

{{examples}}

**Constraints**
- `1 ≤ rows, columns ≤ 6`
- `0 ≤ mine[r][c] ≤ 100`
- At most `20` cells hold gold.
