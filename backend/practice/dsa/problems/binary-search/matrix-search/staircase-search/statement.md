A warehouse stores item codes in a grid where every row is sorted left to right and every column is sorted top to bottom (both non-decreasing). Unlike a seat map, a row may start with a smaller code than the previous row ended with.

Return `true` if `target` is somewhere in the grid.

{{examples}}

**Constraints**
- `1 ≤ m, n ≤ 1000`
- `-10⁹ ≤ grid[i][j], target ≤ 10⁹`
- Rows and columns are sorted in non-decreasing order.
