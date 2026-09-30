A surveyor maps a field as a grid: `land[r][c]` is `'1'` if the cell is clear and `'0'` if it has rocks. A builder needs one rectangular plot, aligned with the grid, made only of clear cells.

Return the area (number of cells) of the largest such plot, or `0` if there are no clear cells.

{{examples}}

**Constraints**
- `1 ≤ land.length, land[r].length ≤ 500`
- All rows have the same length.
- `land[r][c]` is `'0'` or `'1'`.
