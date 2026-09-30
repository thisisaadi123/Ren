An `n × n` chessboard has lost some squares: `holes[i] = [r, c]` means the square in row `r`, column `c` is missing, and no piece can stand there. A queen still attacks along its whole row, column and both diagonals, straight across any holes.

Count the ways to place `n` queens on the board so that no two queens attack each other.

{{examples}}

**Constraints**
- `1 ≤ n ≤ 11`
- `0 ≤ holes.length ≤ n²`
- `holes[i] = [r, c]` with `0 ≤ r, c < n`
- The holes are distinct.
