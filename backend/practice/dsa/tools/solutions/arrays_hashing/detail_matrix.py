"""In-depth text for the matrix-traversal problems (merged into their sol() calls via sol.EXTRA)."""
from sol import EXTRA, table


def grid_table(g, label="r \\ c"):
    return table([label] + list(range(len(g[0]))), *[[r] + list(row) for r, row in enumerate(g)])


COORDS = """
**Think in coordinates.** Every grid transformation is a rule that sends cell `(r, c)` somewhere else. Write the rule
down first, check it on a corner or two, and the code follows:

- flip over the main diagonal: `(r, c) → (c, r)`;
- rotate 90° clockwise in an `n × n` grid: `(r, c) → (c, n − 1 − r)`;
- a spiral read: a sequence of straight walks along shrinking borders.
"""


# ---------------------------------------------------------------- flip-the-grid
fg = [[1, 2, 3], [4, 5, 6]]
ft = [[fg[r][c] for r in range(len(fg))] for c in range(len(fg[0]))]
EXTRA["flip-the-grid"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Non-square grids change shape: `m × n` becomes `n × m`, so a new grid is needed.
        - A single row becomes a single column, and vice versa.
        - A `1 × 1` grid is unchanged.
        """
    ],
    "think": [
        COORDS,
        f"**`{fg}`:**",
        grid_table(fg),
        "**After `(r, c) → (c, r)`:**",
        grid_table(ft),
        "Each column of the input, read top to bottom, becomes a row of the output.",
    ],
    "approaches": {
        0: {
            "idea": [
                """
                Allocate an `n × m` grid and copy `grid[r][c]` into `out[c][r]` for every cell.

                **Why not in place?** For a non-square grid the output has a different shape, so it can't share the input's
                storage. (For square grids, swapping `(r, c)` with `(c, r)` above the diagonal works in place, as in the
                photo rotation.)
                """
            ],
            "build": ["Read the dimensions.", "Allocate `n × m`.", "Copy each cell to its mirrored position."],
            "complexity": ["**Time O(m · n):** each cell copied once. **Space O(m · n)** for the output."],
        },
    },
    "takeaways": [
        """
        - **Transpose:** `out[c][r] = grid[r][c]`.
        - Non-square → new grid; square → swap across the diagonal in place.
        - **Pitfall:** allocating `m × n` instead of `n × m`.
        """
    ],
}


# ---------------------------------------------------------------- rotate-the-photo
p = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
n = len(p)
tr = [[p[c][r] for c in range(n)] for r in range(n)]
rot = [row[::-1] for row in tr]
EXTRA["rotate-the-photo"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - `n = 1`: nothing changes.
        - Odd `n`: the centre cell stays put.
        - In place means no second `n × n` grid.
        """
    ],
    "think": [
        COORDS,
        "**The photo:**",
        grid_table(p),
        f"""
        **Where does each cell go?** Rotating clockwise, the top row becomes the right column, so `(r, c) → (c, n − 1 − r)`.
        Check a corner: `(0, 0)` (value 1) goes to `(0, {n - 1})`, the top-right. ✓

        **Two easy steps instead of one hard one.** `(r, c) → (c, n − 1 − r)` is the composition of
        **transpose** `(r, c) → (c, r)` and **reverse each row** `(c, r) → (c, n − 1 − r)`. Both are easy in place:
        """,
        "**After transposing:**",
        grid_table(tr),
        "**After reversing each row (the rotated photo):**",
        grid_table(rot),
    ],
    "approaches": {
        0: {
            "idea": ["Write each pixel into a new grid at `out[c][n − 1 − r]`. Simple, but uses a second grid."],
            "build": ["Allocate `n × n`.", "Copy each pixel to its rotated position."],
            "complexity": ["**Time O(n²).** **Space O(n²)** for the copy."],
            "limits": ["Needs a whole second grid. Rotating cells in place avoids it."],
        },
        1: {
            "idea": [
                """
                Rotate ring by ring. In each ring, every cell on the top edge belongs to a cycle of four cells (top → right
                → bottom → left) that rotate into each other. Save the top cell, then shift the other three along, and put
                the saved value in the last place.
                """
            ],
            "build": ["For each ring from the outside in.", "For each position along its top edge.", "Rotate the four cells of that cycle."],
            "complexity": ["**Time O(n²):** each cell moves once. **Space O(1).**"],
            "limits": ["Correct, but the index arithmetic for the four corners is easy to get wrong. Transpose plus reverse is the same rotation built from two simple steps."],
        },
        2: {
            "idea": [
                """
                Transpose in place (swap `(r, c)` with `(c, r)` for `c > r`), then reverse every row.

                **Why it's the rotation.** After the transpose, the value from `(r, c)` sits at `(c, r)`; reversing row `c`
                moves it to `(c, n − 1 − r)`, which is exactly the clockwise rotation.
                """
            ],
            "build": ["Swap across the main diagonal (only above it, or each pair would swap twice).", "Reverse each row."],
            "complexity": ["**Time O(n²).** **Space O(1).**"],
        },
    },
    "takeaways": [
        """
        - **Rotate clockwise = transpose + reverse rows**; counter-clockwise = transpose + reverse columns.
        - Write the coordinate rule first, then decompose it into simple in-place steps.
        - **Pitfall:** swapping every `(r, c)` pair in the transpose (each pair swaps twice and nothing changes).
        """
    ],
}


# ---------------------------------------------------------------- spiral-readout
sg = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
top, bottom, left, right = 0, len(sg) - 1, 0, len(sg[0]) - 1
srows = []
while top <= bottom and left <= right:
    srows.append(("top row →", top, [sg[top][c] for c in range(left, right + 1)], f"top = {top + 1}"))
    top += 1
    srows.append(("right column ↓", right, [sg[r][right] for r in range(top, bottom + 1)], f"right = {right - 1}"))
    right -= 1
    if top <= bottom:
        srows.append(("bottom row ←", bottom, [sg[bottom][c] for c in range(right, left - 1, -1)], f"bottom = {bottom - 1}"))
        bottom -= 1
    if left <= right:
        srows.append(("left column ↑", left, [sg[r][left] for r in range(bottom, top - 1, -1)], f"left = {left + 1}"))
        left += 1
order = [v for row in srows for v in row[2]]
EXTRA["spiral-readout"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - A single row or a single column: the spiral is just a straight line.
        - Non-square grids end with a leftover row or column in the middle.
        - Every value must be read exactly once.
        """
    ],
    "think": [
        """
        **Four shrinking borders.** Keep `top`, `bottom`, `left` and `right`, the rows and columns not yet read. One lap
        reads the top row left to right (then `top` moves down), the right column downwards (`right` moves in), the
        bottom row right to left (`bottom` moves up) and the left column upwards (`left` moves in).

        **The two guards.** After reading the top row and right column, the remaining part may have run out of rows or
        columns (a single middle row or column). Reading the bottom row then would re-read the row we just read, so check
        `top ≤ bottom` before it and `left ≤ right` before the left column.
        """,
        "**The grid:**",
        grid_table(sg),
        "**The walks:**",
        table(["walk", "row/column", "values read", "border update"], *[(w, i, v or "—", u) for w, i, v, u in srows]),
        f"Spiral order: **{order}**.",
    ],
    "approaches": {
        0: {
            "idea": [
                """
                Walk like a robot: move in the current direction (right, down, left, up), and turn clockwise whenever the
                next cell would leave the grid or was already visited. A visited grid records which cells are done.
                """
            ],
            "build": ["Visited grid and four direction vectors.", "Read the current cell and mark it.", "Turn if the next cell is blocked.", "Step."],
            "complexity": ["**Time O(m · n).** **Space O(m · n)** for the visited grid."],
            "limits": ["The visited grid is extra memory. Four border variables carry the same information."],
        },
        1: {
            "idea": [
                """
                Read the four sides of the current border, shrinking it after each side, until the borders cross.

                **Why every cell is read once.** Each side reads cells strictly inside the current borders and then moves
                that border inward past them, so no cell is in range twice.
                """
            ],
            "build": ["Four borders.", "Top row, right column, then (guarded) bottom row and left column.", "Shrink after each side."],
            "complexity": ["**Time O(m · n).** **Space O(1)** besides the output."],
            "lines": {
                "borders": "The rows and columns that haven't been read yet.",
                "loop": "While at least one row and one column remain.",
                "top": "Read the top row left to right; that row is done.",
                "right": "Read the right column downwards (below the old top row); that column is done.",
                "bottom": "Only if a row remains: read the bottom row right to left.",
                "left": "Only if a column remains: read the left column upwards.",
                "ret": "Every value, in spiral order.",
            },
        },
    },
    "takeaways": [
        """
        - **Spiral traversal:** four shrinking borders, with guards for a leftover middle row or column.
        - **Pitfall:** reading the last middle row twice when `top > bottom` after the first two sides.
        - The same border bookkeeping generates a spiral (filling a grid in spiral order).
        """
    ],
}


# ---------------------------------------------------------------- blackout-lines
g = [[5, 2, 7, 1], [3, 0, 4, 6], [8, 9, 2, 0], [1, 4, 6, 3]]
m, nn = len(g), len(g[0])
zr = {r for r in range(m) for c in range(nn) if g[r][c] == 0}
zc = {c for r in range(m) for c in range(nn) if g[r][c] == 0}
res = [[0 if r in zr or c in zc else g[r][c] for c in range(nn)] for r in range(m)]
EXTRA["blackout-lines"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Only **original** zeros cause blackouts; zeros created by the blackout must not spread further.
        - A zero in the first row or column, which the O(1)-space method uses as storage.
        - A grid with no zeros is unchanged.
        """
    ],
    "think": [
        """
        **The trap.** Painting rows and columns as soon as a zero is found creates new zeros, which then look like dead
        pixels and black out everything. So first *find* which rows and columns are dark, then paint.
        """,
        "**The grid:**",
        grid_table(g),
        f"""
        Dead pixels in rows {sorted(zr)} and columns {sorted(zc)}. **Result:**
        """,
        grid_table(res),
        """
        **Storing the marks inside the grid.** The flags "row r is dark" and "column c is dark" can live in the grid's
        own first column and first row: for an inner zero at `(r, c)`, set `grid[r][0] = 0` and `grid[0][c] = 0`. Those
        cells will be painted anyway. The first row and column themselves need two extra booleans, recorded *before* any
        marks are written, and they're painted last so their marks are read first.
        """,
    ],
    "approaches": {
        0: {
            "idea": ["Copy the grid. For every original zero, paint its row and column in the copy. Reading from the original keeps new zeros from spreading."],
            "build": ["Copy.", "For each original zero, paint its row and column in the copy."],
            "complexity": ["**Time O(m · n · (m + n))** in the worst case (many zeros). **Space O(m · n)** for the copy."],
            "limits": ["Repaints the same lines for every zero on them, and keeps a whole copy. Recording which lines are dark is enough."],
        },
        1: {
            "idea": ["Two boolean arrays: `zero_row[r]` and `zero_col[c]`. One pass records them, a second paints every cell whose row or column is flagged."],
            "build": ["Flag arrays.", "Record original zeros.", "Paint flagged rows and columns."],
            "complexity": ["**Time O(m · n).** **Space O(m + n).**"],
            "limits": ["The flags use O(m + n) memory; the grid's own first row and column can hold them."],
        },
        2: {
            "idea": [
                """
                1. Remember whether the first row and first column originally contain a zero (`row0`, `col0`).
                2. For each zero in the inner grid, mark `grid[r][0]` and `grid[0][c]`.
                3. Paint inner cells whose row mark or column mark is 0.
                4. Finally paint the first row if `row0`, and the first column if `col0`.

                **Why the order matters.** The marks are read in step 3, so the first row and column must not be painted
                before then; and `row0`/`col0` must be saved before step 2 overwrites those cells.
                """
            ],
            "build": ["Save whether the first row/column had zeros.", "Mark inner zeros on the edges.", "Paint the inner grid from the marks.", "Paint the edges last."],
            "complexity": ["**Time O(m · n).** **Space O(1).**"],
            "lines": {
                "save": "Record whether the first row and first column contained a zero before they're used as storage.",
                "mark": "An inner zero marks its row in column 0 and its column in row 0; those cells would be painted anyway.",
                "paint": "Paint every inner cell whose row or column is marked.",
                "edges": "Paint the first row and column last, from the saved booleans, so their marks were read first.",
                "ret": "The grid after the blackout.",
            },
        },
    },
    "takeaways": [
        """
        - **Find first, then modify**, when changes would trigger more changes.
        - **O(1)-space flags:** store row/column marks in the grid's first row and column; save their own state first.
        - **Pitfall:** painting the first row before reading the marks stored in it.
        """
    ],
}
