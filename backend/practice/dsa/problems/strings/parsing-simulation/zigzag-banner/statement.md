A banner writes `text` in a zigzag over `rows` rows. The first character goes on row `0`, the next on row `1`, and so on down to the last row; then the characters climb back up one row at a time to row `0`, go down again, and so on. With one row, every character stays on row `0`.

The banner's **code** is what you get by reading row `0` from left to right, then row `1`, and so on down to the last row. Return the code.

{{examples}}

**Constraints**
- `1 ≤ text.length ≤ 10⁵`
- `1 ≤ rows ≤ 1000`
- `text` has English letters, digits, `.` and `,`
