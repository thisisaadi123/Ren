A puzzle designer is sketching `n × n` boards with `n` queens where no two queens attack each other (no shared row, column or diagonal). A few queens are already glued down: each `fixed[i] = [r, c]` is a queen at row `r`, column `c`.

Return every complete layout that keeps all the glued queens. Draw each layout as `n` strings, one per row from top to bottom, with `'Q'` for a queen and `'.'` for an empty square. The layouts may be returned in any order; if the glued queens already attack each other, or no layout fits, return an empty list.

{{examples}}

**Constraints**
- `1 ≤ n ≤ 9`
- `0 ≤ fixed.length ≤ n`
- `fixed[i] = [r, c]` with `0 ≤ r, c < n`
- The squares in `fixed` are distinct.
