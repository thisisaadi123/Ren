A petri dish is a grid `board` where `1` is a living cell and `0` is empty. Each cell has up to eight neighbours: horizontal, vertical and diagonal. One generation later:

- A living cell with **2 or 3** living neighbours stays alive; any other living cell dies.
- An empty cell with **exactly 3** living neighbours comes alive.

Every cell changes at the same moment, based on the board as it was. Return the board after one generation. Try it without a second grid.

{{examples}}

**Constraints**
- `1 ≤ board.length, board[i].length ≤ 200`
- All rows have the same length.
- `board[i][j]` is `0` or `1`.
