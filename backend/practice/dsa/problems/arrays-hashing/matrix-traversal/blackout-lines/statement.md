A display is a grid of brightness values. Whenever a pixel is dead (value `0`), its whole row and whole column go dark.

Return the grid after every dead pixel's row and column are set to `0`. Only the pixels that were `0` in the original grid cause blackouts.

{{examples}}

**Constraints**
- `1 ≤ m, n ≤ 300`
- `-10⁹ ≤ grid[r][c] ≤ 10⁹`
