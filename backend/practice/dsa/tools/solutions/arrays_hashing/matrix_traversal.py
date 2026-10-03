"""Arrays & Hashing: matrix traversal."""
from sol import Grid, Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401



@problem
def blackout_lines():
    g = [[5, 2, 7, 1], [3, 0, 4, 6], [8, 9, 2, 0], [1, 4, 6, 3]]
    m, n = len(g), len(g[0])
    zr = {r for r in range(m) if 0 in g[r]}
    zc = {c for c in range(n) if any(g[r][c] == 0 for r in range(m))}
    res = [[0 if r in zr or c in zc else g[r][c] for c in range(n)] for r in range(m)]

    w1 = Steps("Copy the grid. For each 0 in the original, black out its row and column in the copy.")
    out = [row[:] for row in g]
    for r in range(m):
        for c in range(n):
            if g[r][c] == 0:
                for k in range(n):
                    out[r][k] = 0
                for k in range(m):
                    out[k][c] = 0
                st = {(r, k): "mark" for k in range(n)} | {(k, c): "mark" for k in range(m)}
                st[(r, c)] = "active"
                w1.step(f"Original ({r}, {c}) is 0: zero row {r} and column {c} in the copy.", Grid([row[:] for row in out], st=st, label="copy"))
    w1.step("Every original zero handled. Zeros we wrote never trigger more blackouts, because we only look at the original.", Grid(out, label="result"), result=res)

    w2 = Steps("Record which rows and which columns contain a 0, then zero every cell in a marked row or column.")
    w2.step(f"Scan once: rows {sorted(zr)} and columns {sorted(zc)} contain a 0.", Grid(g, st={(r, c): "active" for r in range(m) for c in range(n) if g[r][c] == 0}), Row(["x" if r in zr else None for r in range(m)], label="row has 0"), Row(["x" if c in zc else None for c in range(n)], label="column has 0"))
    w2.step("Second scan: a cell becomes 0 if its row or its column is marked.", Grid(res, st={(r, c): "new" for r in range(m) for c in range(n) if r in zr or c in zc}), result=res)

    w3 = Steps("Use row 0 and column 0 themselves as the markers; two booleans remember whether they had zeros of their own.")
    a = [row[:] for row in g]
    r0 = 0 in a[0]
    c0 = any(a[r][0] == 0 for r in range(m))
    w3.step(f"First: does row 0 contain a 0 of its own? {'Yes' if r0 else 'No'}. Does column 0? {'Yes' if c0 else 'No'}. Save that, because row 0 and column 0 are about to hold markers.", Grid(a, st={(0, c): "mark" for c in range(n)} | {(r, 0): "mark" for r in range(m)}), Vars(row0_zero=r0, col0_zero=c0))
    for r in range(1, m):
        for c in range(1, n):
            if a[r][c] == 0:
                a[r][0] = 0
                a[0][c] = 0
    w3.step("For each 0 inside (rows ≥ 1, columns ≥ 1), write a 0 into the first cell of its row and its column.", Grid([row[:] for row in a], st={(r, 0): "new" for r in range(1, m) if a[r][0] == 0} | {(0, c): "new" for c in range(1, n) if a[0][c] == 0}))
    for r in range(1, m):
        for c in range(1, n):
            if a[r][0] == 0 or a[0][c] == 0:
                a[r][c] = 0
    w3.step("Zero every inner cell whose row marker or column marker is 0.", Grid([row[:] for row in a]))
    if r0:
        a[0] = [0] * n
    if c0:
        for r in range(m):
            a[r][0] = 0
    w3.step("Finally blank row 0 and/or column 0 if they had their own zeros. (Here neither did.)" if not (r0 or c0) else "Finally blank row 0 and/or column 0 using the saved booleans.", Grid(a), result=res)
    assert a == res

    sol(
        "blackout-lines",
        summary="""
            Decide first, then paint: record which rows and columns contain an original 0, and only afterwards set
            cells to 0. Painting while scanning would let new zeros cause blackouts of their own. The records can
            live in two small arrays, or, for O(1) extra space, in the grid's own first row and first column.
        """,
        question=[
            """
            Every pixel that is 0 in the **original** grid blacks out its entire row and entire column. Return the
            resulting grid.

            - **Only original zeros count.** A pixel that becomes 0 because of a blackout must not trigger another
              blackout; otherwise one zero would wipe out the whole grid.
            - **Values can be negative or large,** so there's no spare "special" value to use as a marker except
              0 itself.
            - **Size:** up to 300 × 300.
            """
        ],
        think=[
            """
            Take this 4 × 4 grid with zeros at (1, 1) and (2, 3). Rows 1 and 2, and columns 1 and 3, go dark.
            """,
            fig(Grid(g, st={(1, 1): "active", (2, 3): "active"}, label="original"), Grid(res, st={(r, c): "mark" for r in range(m) for c in range(n) if res[r][c] == 0}, label="after blackout")),
            """
            The trap: if you zero row 1 as soon as you find (1, 1), then cell (1, 2) becomes 0, and when the scan
            reaches it, it looks like an original zero and blacks out column 2 too. Wrong.

            So separate **deciding** from **painting**. All you need to decide is *which rows* and *which columns*
            contain an original 0: that's m + n yes/no answers, not m × n.
            """,
        ],
        approaches=[
            approach(
                "Paint into a copy for each zero",
                "brute",
                "O(m · n · (m + n))",
                "O(m · n)",
                idea=["Copy the grid. Scan the **original**; for each 0 found, set its whole row and column to 0 **in the copy**. Since decisions come from the untouched original, painted zeros never spread."],
                walk=w1,
                build=["Copy the grid.", "For every original cell equal to 0: zero row r and column c in the copy.", "Return the copy."],
                code={
                    "python": """
                        class Solution:
                            def blackout(self, grid: List[List[int]]) -> List[List[int]]:
                                m, n = len(grid), len(grid[0])
                                out = [row[:] for row in grid]  #@copy
                                for r in range(m):  #@scan
                                    for c in range(n):  #@scan
                                        if grid[r][c] == 0:  #@scan
                                            for k in range(n):  #@paint
                                                out[r][k] = 0  #@paint
                                            for k in range(m):  #@paint
                                                out[k][c] = 0  #@paint
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[][] blackout(int[][] grid) {
                                int m = grid.length, n = grid[0].length;
                                int[][] out = new int[m][];  //@copy
                                for (int r = 0; r < m; r++) out[r] = grid[r].clone();  //@copy
                                for (int r = 0; r < m; r++)  //@scan
                                    for (int c = 0; c < n; c++)  //@scan
                                        if (grid[r][c] == 0) {  //@scan
                                            for (int k = 0; k < n; k++) out[r][k] = 0;  //@paint
                                            for (int k = 0; k < m; k++) out[k][c] = 0;  //@paint
                                        }
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<vector<int>> blackout(vector<vector<int>>& grid) {
                                int m = grid.size(), n = grid[0].size();
                                vector<vector<int>> out = grid;  //@copy
                                for (int r = 0; r < m; r++)  //@scan
                                    for (int c = 0; c < n; c++)  //@scan
                                        if (grid[r][c] == 0) {  //@scan
                                            for (int k = 0; k < n; k++) out[r][k] = 0;  //@paint
                                            for (int k = 0; k < m; k++) out[k][c] = 0;  //@paint
                                        }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int** blackout(int** grid, int gridSize, int* gridColSize, int* returnSize, int** returnColumnSizes) {
                            int m = gridSize, n = gridColSize[0];
                            int** out = malloc(m * sizeof(int*));  //@copy
                            for (int r = 0; r < m; r++) {  //@copy
                                out[r] = malloc(n * sizeof(int));  //@copy
                                memcpy(out[r], grid[r], n * sizeof(int));  //@copy
                            }  //@copy
                            for (int r = 0; r < m; r++)  //@scan
                                for (int c = 0; c < n; c++)  //@scan
                                    if (grid[r][c] == 0) {  //@scan
                                        for (int k = 0; k < n; k++) out[r][k] = 0;  //@paint
                                        for (int k = 0; k < m; k++) out[k][c] = 0;  //@paint
                                    }
                            *returnSize = m;  //@ret
                            *returnColumnSizes = malloc(m * sizeof(int));  //@ret
                            for (int i = 0; i < m; i++) (*returnColumnSizes)[i] = n;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("copy", "The result starts as a copy; the original is only ever read."),
                    ("scan", "Find the original zeros."),
                    ("paint", "Black out the zero's row and column in the copy."),
                    ("ret", "The blacked-out grid.", {"c": "Report the row count and each row's length."}),
                ],
                complexity=["**Time O(m · n · (m + n))**: up to m · n zeros, each painting m + n cells. **Space O(m · n)** for the copy."],
                limits=["Rows and columns get painted over and over (a row with 50 zeros is blacked out 50 times), and the copy costs a whole grid. Only *which* rows and columns are affected matters."],
                slow=True,
            ),
            approach(
                "Row and column flags",
                "better",
                "O(m · n)",
                "O(m + n)",
                idea=["One pass fills `zeroRow[r]` and `zeroCol[c]` for every original 0. A second pass sets a cell to 0 if its row or its column is flagged. Deciding happens entirely before painting."],
                walk=w2,
                build=["Make `zeroRow` (size m) and `zeroCol` (size n).", "First pass: for every 0 at (r, c), set both flags.", "Second pass: zero every cell with `zeroRow[r] or zeroCol[c]`.", "Return the grid."],
                code={
                    "python": """
                        class Solution:
                            def blackout(self, grid: List[List[int]]) -> List[List[int]]:
                                m, n = len(grid), len(grid[0])
                                zero_row, zero_col = [False] * m, [False] * n  #@flags
                                for r in range(m):  #@find
                                    for c in range(n):  #@find
                                        if grid[r][c] == 0:  #@find
                                            zero_row[r] = zero_col[c] = True  #@find
                                for r in range(m):  #@paint
                                    for c in range(n):  #@paint
                                        if zero_row[r] or zero_col[c]:  #@paint
                                            grid[r][c] = 0  #@paint
                                return grid  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[][] blackout(int[][] grid) {
                                int m = grid.length, n = grid[0].length;
                                boolean[] zeroRow = new boolean[m], zeroCol = new boolean[n];  //@flags
                                for (int r = 0; r < m; r++)  //@find
                                    for (int c = 0; c < n; c++)  //@find
                                        if (grid[r][c] == 0) zeroRow[r] = zeroCol[c] = true;  //@find
                                for (int r = 0; r < m; r++)  //@paint
                                    for (int c = 0; c < n; c++)  //@paint
                                        if (zeroRow[r] || zeroCol[c]) grid[r][c] = 0;  //@paint
                                return grid;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<vector<int>> blackout(vector<vector<int>>& grid) {
                                int m = grid.size(), n = grid[0].size();
                                vector<bool> zeroRow(m, false), zeroCol(n, false);  //@flags
                                for (int r = 0; r < m; r++)  //@find
                                    for (int c = 0; c < n; c++)  //@find
                                        if (grid[r][c] == 0) zeroRow[r] = zeroCol[c] = true;  //@find
                                for (int r = 0; r < m; r++)  //@paint
                                    for (int c = 0; c < n; c++)  //@paint
                                        if (zeroRow[r] || zeroCol[c]) grid[r][c] = 0;  //@paint
                                return grid;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int** blackout(int** grid, int gridSize, int* gridColSize, int* returnSize, int** returnColumnSizes) {
                            int m = gridSize, n = gridColSize[0];
                            bool* zeroRow = calloc(m, sizeof(bool));  //@flags
                            bool* zeroCol = calloc(n, sizeof(bool));  //@flags
                            for (int r = 0; r < m; r++)  //@find
                                for (int c = 0; c < n; c++)  //@find
                                    if (grid[r][c] == 0) zeroRow[r] = zeroCol[c] = true;  //@find
                            for (int r = 0; r < m; r++)  //@paint
                                for (int c = 0; c < n; c++)  //@paint
                                    if (zeroRow[r] || zeroCol[c]) grid[r][c] = 0;  //@paint
                            free(zeroRow);  //@ret
                            free(zeroCol);  //@ret
                            *returnSize = m;  //@ret
                            *returnColumnSizes = malloc(m * sizeof(int));  //@ret
                            for (int i = 0; i < m; i++) (*returnColumnSizes)[i] = n;  //@ret
                            return grid;  //@ret
                        }
                    """,
                },
                lines=[
                    ("flags", "One flag per row and one per column: m + n booleans instead of a full copy."),
                    ("find", "Every original zero flags its row and its column. No painting yet."),
                    ("paint", "Now paint: a cell goes dark if its row or column was flagged. Flags were decided from the original, so new zeros can't spread."),
                    ("ret", "The grid, updated in place.", {"c": "Free the flags; only the column-size array is new."}),
                ],
                complexity=["**Time O(m · n):** two passes. **Space O(m + n)** for the flags."],
                limits=["m + n extra booleans. The grid's own first row and first column can hold the same flags."],
            ),
            approach(
                "Use the first row and column as the flags",
                "best",
                "O(m · n)",
                "O(1)",
                idea=[
                    """
                    Cell `(r, 0)` can act as row r's flag and `(0, c)` as column c's flag: setting them to 0 is
                    harmless, because a flagged row or column will be zeroed anyway. The only catch is that row 0 and
                    column 0 are themselves real data, so first save two booleans: "row 0 had a zero" and "column 0
                    had a zero".

                    1. Save the two booleans.
                    2. For each inner 0 at (r, c) with r, c ≥ 1, set `grid[r][0] = 0` and `grid[0][c] = 0`.
                    3. Zero every inner cell whose row flag or column flag is 0.
                    4. Zero row 0 and column 0 if their booleans say so. (They're done last, because their cells were
                       the flags.)
                    """
                ],
                walk=w3,
                build=["`row0` = row 0 contains a 0; `col0` = column 0 contains a 0.", "Mark inner zeros into row 0 / column 0.", "Zero inner cells using the marks.", "Zero row 0 if `row0`, column 0 if `col0`."],
                code={
                    "python": """
                        class Solution:
                            def blackout(self, grid: List[List[int]]) -> List[List[int]]:
                                m, n = len(grid), len(grid[0])
                                row0 = any(grid[0][c] == 0 for c in range(n))  #@save
                                col0 = any(grid[r][0] == 0 for r in range(m))  #@save
                                for r in range(1, m):  #@mark
                                    for c in range(1, n):  #@mark
                                        if grid[r][c] == 0:  #@mark
                                            grid[r][0] = grid[0][c] = 0  #@mark
                                for r in range(1, m):  #@paint
                                    for c in range(1, n):  #@paint
                                        if grid[r][0] == 0 or grid[0][c] == 0:  #@paint
                                            grid[r][c] = 0  #@paint
                                if row0:  #@edges
                                    for c in range(n):  #@edges
                                        grid[0][c] = 0  #@edges
                                if col0:  #@edges
                                    for r in range(m):  #@edges
                                        grid[r][0] = 0  #@edges
                                return grid  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[][] blackout(int[][] grid) {
                                int m = grid.length, n = grid[0].length;
                                boolean row0 = false, col0 = false;  //@save
                                for (int c = 0; c < n; c++) if (grid[0][c] == 0) row0 = true;  //@save
                                for (int r = 0; r < m; r++) if (grid[r][0] == 0) col0 = true;  //@save
                                for (int r = 1; r < m; r++)  //@mark
                                    for (int c = 1; c < n; c++)  //@mark
                                        if (grid[r][c] == 0) grid[r][0] = grid[0][c] = 0;  //@mark
                                for (int r = 1; r < m; r++)  //@paint
                                    for (int c = 1; c < n; c++)  //@paint
                                        if (grid[r][0] == 0 || grid[0][c] == 0) grid[r][c] = 0;  //@paint
                                if (row0) for (int c = 0; c < n; c++) grid[0][c] = 0;  //@edges
                                if (col0) for (int r = 0; r < m; r++) grid[r][0] = 0;  //@edges
                                return grid;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<vector<int>> blackout(vector<vector<int>>& grid) {
                                int m = grid.size(), n = grid[0].size();
                                bool row0 = false, col0 = false;  //@save
                                for (int c = 0; c < n; c++) if (grid[0][c] == 0) row0 = true;  //@save
                                for (int r = 0; r < m; r++) if (grid[r][0] == 0) col0 = true;  //@save
                                for (int r = 1; r < m; r++)  //@mark
                                    for (int c = 1; c < n; c++)  //@mark
                                        if (grid[r][c] == 0) grid[r][0] = grid[0][c] = 0;  //@mark
                                for (int r = 1; r < m; r++)  //@paint
                                    for (int c = 1; c < n; c++)  //@paint
                                        if (grid[r][0] == 0 || grid[0][c] == 0) grid[r][c] = 0;  //@paint
                                if (row0) for (int c = 0; c < n; c++) grid[0][c] = 0;  //@edges
                                if (col0) for (int r = 0; r < m; r++) grid[r][0] = 0;  //@edges
                                return grid;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int** blackout(int** grid, int gridSize, int* gridColSize, int* returnSize, int** returnColumnSizes) {
                            int m = gridSize, n = gridColSize[0];
                            bool row0 = false, col0 = false;  //@save
                            for (int c = 0; c < n; c++) if (grid[0][c] == 0) row0 = true;  //@save
                            for (int r = 0; r < m; r++) if (grid[r][0] == 0) col0 = true;  //@save
                            for (int r = 1; r < m; r++)  //@mark
                                for (int c = 1; c < n; c++)  //@mark
                                    if (grid[r][c] == 0) grid[r][0] = grid[0][c] = 0;  //@mark
                            for (int r = 1; r < m; r++)  //@paint
                                for (int c = 1; c < n; c++)  //@paint
                                    if (grid[r][0] == 0 || grid[0][c] == 0) grid[r][c] = 0;  //@paint
                            if (row0) for (int c = 0; c < n; c++) grid[0][c] = 0;  //@edges
                            if (col0) for (int r = 0; r < m; r++) grid[r][0] = 0;  //@edges
                            *returnSize = m;  //@ret
                            *returnColumnSizes = malloc(m * sizeof(int));  //@ret
                            for (int i = 0; i < m; i++) (*returnColumnSizes)[i] = n;  //@ret
                            return grid;  //@ret
                        }
                    """,
                },
                lines=[
                    ("save", "Row 0 and column 0 are about to be used as flag storage, so first remember whether they had original zeros of their own."),
                    ("mark", "An inner zero flags its row (in column 0) and its column (in row 0). Overwriting those cells with 0 loses nothing: that row and column will be zeroed anyway."),
                    ("paint", "Inner cells read their two flags. Row 0 and column 0 aren't touched yet, because they're still being read as flags."),
                    ("edges", "Last, zero row 0 and/or column 0 if they had their own zeros. Doing this earlier would corrupt the flags."),
                    ("ret", "The grid, in place.", {"c": "Only the column-size array is new."}),
                ],
                complexity=["**Time O(m · n).** **Space O(1):** two booleans."],
            ),
        ],
        takeaways=[
            """
            - Never let the effects of an update trigger more updates: **decide first, then paint**.
            - What you need to remember is often much smaller than the grid: here m + n flags.
            - To get O(1) space, store flags inside the data itself (first row/column), saving whatever those cells
              originally meant, and process the flag cells **last**.
            """
        ],
    )


@problem
def flip_the_grid():
    g = [[1, 2, 3], [4, 5, 6]]
    t = [list(c) for c in zip(*g)]
    w = Steps("Make an n × m grid; cell (r, c) of the input goes to (c, r).")
    w.step("A 2 × 3 grid becomes 3 × 2.", Grid(g, label="input 2 × 3"))
    out = [[None] * 2 for _ in range(3)]
    for r in range(2):
        for c in range(3):
            out[c][r] = g[r][c]
            w.step(f"Input ({r}, {c}) = {g[r][c]} → output ({c}, {r}).", Grid(g, st={(r, c): "active"}, label="input"), Grid([row[:] for row in out], st={(c, r): "new"}, label="output 3 × 2"))
    w.step("Rows have become columns.", Grid(t, label="output"), result=t)

    sol(
        "flip-the-grid",
        summary="""
            Transposing sends cell (r, c) to (c, r), so an m × n grid becomes n × m. Allocate the new shape and copy
            each value across: O(m · n), which is optimal since every value must move.
        """,
        question=[
            """
            Flip the grid over its main diagonal: row r, column c moves to row c, column r.

            - **The shape changes** from m × n to n × m. For a non-square grid the result can't fit in the original
              array, so a new grid is required.
            - **Rows become columns:** the first row `[1, 2, 3]` becomes the first column.
            - **Size:** up to 10⁵ cells in total.
            """
        ],
        think=[
            """
            Take `[[1, 2, 3], [4, 5, 6]]`. Read each **column** top to bottom and write it as a **row**:
            column 0 is 1, 4; column 1 is 2, 5; column 2 is 3, 6. Result: `[[1, 4], [2, 5], [3, 6]]`.
            """,
            fig(Grid(g, label="2 × 3"), Grid(t, label="3 × 2")),
            """
            In index terms: `out[c][r] = grid[r][c]`. There's only one sensible way to do this. Every value has to
            be written once, so O(m · n) time is the best possible, and the output itself needs m · n space. The
            only thing to get right is the shape: `out` has **n rows of length m**.
            """,
        ],
        approaches=[
            approach(
                "Copy each cell to its mirrored position",
                "best",
                "O(m · n)",
                "O(m · n)",
                idea=["Create an n × m grid and set `out[c][r] = grid[r][c]` for every cell."],
                walk=w,
                build=["Read m (rows) and n (columns).", "Create `out` with n rows and m columns.", "For every (r, c): `out[c][r] = grid[r][c]`.", "Return `out`."],
                code={
                    "python": """
                        class Solution:
                            def transpose(self, grid: List[List[int]]) -> List[List[int]]:
                                m, n = len(grid), len(grid[0])  #@dims
                                out = [[0] * m for _ in range(n)]  #@alloc
                                for r in range(m):  #@copy
                                    for c in range(n):  #@copy
                                        out[c][r] = grid[r][c]  #@copy
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[][] transpose(int[][] grid) {
                                int m = grid.length, n = grid[0].length;  //@dims
                                int[][] out = new int[n][m];  //@alloc
                                for (int r = 0; r < m; r++)  //@copy
                                    for (int c = 0; c < n; c++)  //@copy
                                        out[c][r] = grid[r][c];  //@copy
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<vector<int>> transpose(vector<vector<int>>& grid) {
                                int m = grid.size(), n = grid[0].size();  //@dims
                                vector<vector<int>> out(n, vector<int>(m));  //@alloc
                                for (int r = 0; r < m; r++)  //@copy
                                    for (int c = 0; c < n; c++)  //@copy
                                        out[c][r] = grid[r][c];  //@copy
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int** transpose(int** grid, int gridSize, int* gridColSize, int* returnSize, int** returnColumnSizes) {
                            int m = gridSize, n = gridColSize[0];  //@dims
                            int** out = malloc(n * sizeof(int*));  //@alloc
                            for (int c = 0; c < n; c++) out[c] = malloc(m * sizeof(int));  //@alloc
                            for (int r = 0; r < m; r++)  //@copy
                                for (int c = 0; c < n; c++)  //@copy
                                    out[c][r] = grid[r][c];  //@copy
                            *returnSize = n;  //@ret
                            *returnColumnSizes = malloc(n * sizeof(int));  //@ret
                            for (int i = 0; i < n; i++) (*returnColumnSizes)[i] = m;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("dims", "m rows and n columns in the input."),
                    ("alloc", "The output has the swapped shape: n rows, each of length m."),
                    ("copy", "Each value moves from (r, c) to (c, r)."),
                    ("ret", "The transposed grid.", {"c": "n rows, each of length m."}),
                ],
                complexity=[
                    """
                    **Time O(m · n):** each value is copied once, and no algorithm can do less.

                    **Space O(m · n)** for the output (required, since the shape changes). For a **square** grid you
                    could transpose in place by swapping `grid[r][c]` with `grid[c][r]` for `c > r` (see
                    **Rotate the Photo**).
                    """
                ],
            ),
        ],
        takeaways=[
            """
            - Transpose: `out[c][r] = grid[r][c]`, with the output shaped n × m.
            - Square grids can be transposed in place by swapping across the diagonal (only `c > r`, or every pair
              is swapped twice and nothing changes).
            - Transposing is a building block: transpose + reverse each row = rotate 90° clockwise.
            """
        ],
    )


@problem
def rotate_the_photo():
    p = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
    n = len(p)
    rot = [list(r) for r in zip(*p[::-1])]

    w1 = Steps("Write each pixel into a new grid: (r, c) goes to (c, n − 1 − r).")
    out = [[None] * n for _ in range(n)]
    for r in range(n):
        for c in range(n):
            out[c][n - 1 - r] = p[r][c]
        w1.step(f"Row {r} of the photo becomes column {n - 1 - r} of the result.", Grid(p, st={(r, c): "active" for c in range(n)}, label="photo"), Grid([row[:] for row in out], st={(c, n - 1 - r): "new" for c in range(n)}, label="new grid"))
    w1.step("Done.", Grid(rot, label="rotated"), result=rot)

    w2 = Steps("Rotate ring by ring: each group of four cells moves one corner clockwise.")
    a = [row[:] for row in p]
    for layer in range(n // 2):
        first, last = layer, n - 1 - layer
        for i in range(first, last):
            off = i - first
            cells = [(first, i), (i, last), (last, last - off), (last - off, first)]
            top = a[first][i]
            a[first][i] = a[last - off][first]
            a[last - off][first] = a[last][last - off]
            a[last][last - off] = a[i][last]
            a[i][last] = top
            w2.step(f"Ring {layer}: the four cells {', '.join(map(str, cells))} rotate together (left → top → right → bottom → left).", Grid([row[:] for row in a], st={c: "new" for c in cells}))
    w2.step("Every ring done.", Grid(a), result=rot)

    w3 = Steps("Transpose (swap across the diagonal), then reverse every row.")
    a = [row[:] for row in p]
    for r in range(n):
        for c in range(r + 1, n):
            a[r][c], a[c][r] = a[c][r], a[r][c]
    w3.step("Step 1, transpose: swap (r, c) with (c, r) for every c > r. Row 0 is now the old column 0.", Grid(p, label="photo"), Grid([row[:] for row in a], label="transposed"))
    for row in a:
        row.reverse()
    w3.step("Step 2, reverse each row. The old column 0 (1, 5, 9, 13) now reads 13, 9, 5, 1 across the top: exactly a clockwise turn.", Grid(a, label="rotated"), result=rot)

    sol(
        "rotate-the-photo",
        summary="""
            A 90° clockwise turn sends (r, c) to (c, n − 1 − r). In place, that's two simple, reversible steps:
            **transpose** (swap across the diagonal), then **reverse each row**. Both are O(n²) with O(1) extra space
            and hard to get wrong.
        """,
        question=[
            """
            Rotate a square n × n grid 90 degrees clockwise.

            - **Clockwise:** the left column becomes the top row (read bottom to top), and the top row becomes the
              right column.
            - **In place** is the challenge: modify the given grid without a second n × n grid.
            - **Square only**, so the shape doesn't change. n can be odd; the centre cell stays put.
            """
        ],
        think=[
            """
            Take the 4 × 4 photo numbered 1 to 16. After the turn, the top row is the old **left column read from
            bottom to top**: 13, 9, 5, 1.
            """,
            fig(Grid(p, label="photo"), Grid(rot, label="rotated clockwise")),
            """
            Track one cell to find the rule: 2 sits at (0, 1) and ends at (1, 3). In general (r, c) → (c, n − 1 − r).

            That mapping is two simpler moves composed:

            - **(r, c) → (c, r)** is a transpose (mirror over the main diagonal);
            - **(c, r) → (c, n − 1 − r)** is a left-right mirror within each row.

            Both can be done in place with swaps. Alternatively, the rotation moves cells in **cycles of four**
            (corner to corner around each ring), which can also be done in place with one temporary variable.
            """,
        ],
        approaches=[
            approach(
                "Write into a new grid",
                "better",
                "O(n²)",
                "O(n²)",
                idea=["Allocate an n × n grid and set `out[c][n − 1 − r] = photo[r][c]` for every cell."],
                walk=w1,
                build=["Create an n × n grid.", "For each (r, c): `out[c][n − 1 − r] = photo[r][c]`.", "Return it."],
                code={
                    "python": """
                        class Solution:
                            def rotateClockwise(self, photo: List[List[int]]) -> List[List[int]]:
                                n = len(photo)
                                out = [[0] * n for _ in range(n)]  #@alloc
                                for r in range(n):  #@move
                                    for c in range(n):  #@move
                                        out[c][n - 1 - r] = photo[r][c]  #@move
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[][] rotateClockwise(int[][] photo) {
                                int n = photo.length;
                                int[][] out = new int[n][n];  //@alloc
                                for (int r = 0; r < n; r++)  //@move
                                    for (int c = 0; c < n; c++)  //@move
                                        out[c][n - 1 - r] = photo[r][c];  //@move
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<vector<int>> rotateClockwise(vector<vector<int>>& photo) {
                                int n = photo.size();
                                vector<vector<int>> out(n, vector<int>(n));  //@alloc
                                for (int r = 0; r < n; r++)  //@move
                                    for (int c = 0; c < n; c++)  //@move
                                        out[c][n - 1 - r] = photo[r][c];  //@move
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int** rotateClockwise(int** photo, int photoSize, int* photoColSize, int* returnSize, int** returnColumnSizes) {
                            int n = photoSize;
                            int** out = malloc(n * sizeof(int*));  //@alloc
                            for (int r = 0; r < n; r++) out[r] = malloc(n * sizeof(int));  //@alloc
                            for (int r = 0; r < n; r++)  //@move
                                for (int c = 0; c < n; c++)  //@move
                                    out[c][n - 1 - r] = photo[r][c];  //@move
                            *returnSize = n;  //@ret
                            *returnColumnSizes = malloc(n * sizeof(int));  //@ret
                            for (int i = 0; i < n; i++) (*returnColumnSizes)[i] = n;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("alloc", "A second n × n grid."),
                    ("move", "Row r of the photo becomes column n − 1 − r of the result; position c along the row becomes row c."),
                    ("ret", "The rotated photo.", {"c": "Report n rows of length n."}),
                ],
                complexity=["**Time O(n²).** **Space O(n²)** for the second grid."],
                limits=["The problem asks for no second grid. Since a rotation only permutes cells, it can be done by swapping inside the original."],
            ),
            approach(
                "Rotate four cells at a time, ring by ring",
                "better",
                "O(n²)",
                "O(1)",
                idea=[
                    """
                    Each cell belongs to a cycle of four: top → right → bottom → left → top. For each ring (layer) from the
                    outside in, and each position `i` along its top edge (except the last, which is the next corner),
                    save the top cell, then move left → top, bottom → left, right → bottom, saved top → right.
                    """
                ],
                walk=w2,
                build=["For each `layer` in `0 … n/2 − 1`, let `first = layer`, `last = n − 1 − layer`.", "For each `i` from `first` to `last − 1`, with `off = i − first`:", "`top = a[first][i]`; `a[first][i] = a[last − off][first]`; `a[last − off][first] = a[last][last − off]`; `a[last][last − off] = a[i][last]`; `a[i][last] = top`."],
                code={
                    "python": """
                        class Solution:
                            def rotateClockwise(self, photo: List[List[int]]) -> List[List[int]]:
                                n = len(photo)
                                for layer in range(n // 2):  #@ring
                                    first, last = layer, n - 1 - layer  #@ring
                                    for i in range(first, last):  #@pos
                                        off = i - first  #@pos
                                        top = photo[first][i]  #@cycle
                                        photo[first][i] = photo[last - off][first]  #@cycle
                                        photo[last - off][first] = photo[last][last - off]  #@cycle
                                        photo[last][last - off] = photo[i][last]  #@cycle
                                        photo[i][last] = top  #@cycle
                                return photo  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[][] rotateClockwise(int[][] photo) {
                                int n = photo.length;
                                for (int layer = 0; layer < n / 2; layer++) {  //@ring
                                    int first = layer, last = n - 1 - layer;  //@ring
                                    for (int i = first; i < last; i++) {  //@pos
                                        int off = i - first;  //@pos
                                        int top = photo[first][i];  //@cycle
                                        photo[first][i] = photo[last - off][first];  //@cycle
                                        photo[last - off][first] = photo[last][last - off];  //@cycle
                                        photo[last][last - off] = photo[i][last];  //@cycle
                                        photo[i][last] = top;  //@cycle
                                    }
                                }
                                return photo;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<vector<int>> rotateClockwise(vector<vector<int>>& photo) {
                                int n = photo.size();
                                for (int layer = 0; layer < n / 2; layer++) {  //@ring
                                    int first = layer, last = n - 1 - layer;  //@ring
                                    for (int i = first; i < last; i++) {  //@pos
                                        int off = i - first;  //@pos
                                        int top = photo[first][i];  //@cycle
                                        photo[first][i] = photo[last - off][first];  //@cycle
                                        photo[last - off][first] = photo[last][last - off];  //@cycle
                                        photo[last][last - off] = photo[i][last];  //@cycle
                                        photo[i][last] = top;  //@cycle
                                    }
                                }
                                return photo;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int** rotateClockwise(int** photo, int photoSize, int* photoColSize, int* returnSize, int** returnColumnSizes) {
                            int n = photoSize;
                            for (int layer = 0; layer < n / 2; layer++) {  //@ring
                                int first = layer, last = n - 1 - layer;  //@ring
                                for (int i = first; i < last; i++) {  //@pos
                                    int off = i - first;  //@pos
                                    int top = photo[first][i];  //@cycle
                                    photo[first][i] = photo[last - off][first];  //@cycle
                                    photo[last - off][first] = photo[last][last - off];  //@cycle
                                    photo[last][last - off] = photo[i][last];  //@cycle
                                    photo[i][last] = top;  //@cycle
                                }
                            }
                            *returnSize = n;  //@ret
                            *returnColumnSizes = malloc(n * sizeof(int));  //@ret
                            for (int i = 0; i < n; i++) (*returnColumnSizes)[i] = n;  //@ret
                            return photo;  //@ret
                        }
                    """,
                },
                lines=[
                    ("ring", "Rings from the outside in. `first` and `last` are the ring's first and last row/column. The centre cell of an odd n is never touched."),
                    ("pos", "Each position along the top edge, except the last (that's the next corner, handled as part of the first cycle). `off` is how far along the edge we are."),
                    ("cycle", "Four cells move at once with one temporary: save top; left moves up; bottom moves left; right moves down; saved top moves right. Each assignment reads a cell before it's overwritten."),
                    ("ret", "Rotated in place."),
                ],
                complexity=["**Time O(n²):** each cell is moved once. **Space O(1).**"],
                limits=["Correct and optimal, but the index arithmetic (`last − off` in two places) is easy to get wrong under pressure. The next approach reaches the same result with two operations you can verify at a glance."],
            ),
            approach(
                "Transpose, then reverse each row",
                "best",
                "O(n²)",
                "O(1)",
                idea=[
                    """
                    The rotation (r, c) → (c, n − 1 − r) equals a transpose (r, c) → (c, r) followed by mirroring each
                    row (c, r) → (c, n − 1 − r). Both are in-place swaps:

                    - **Transpose:** swap `photo[r][c]` with `photo[c][r]` for every `c > r` (only above the diagonal,
                      or each pair would be swapped back).
                    - **Reverse each row:** swap from both ends towards the middle.
                    """
                ],
                walk=w3,
                build=["For r in 0 … n−1 and c in r+1 … n−1: swap `photo[r][c]` and `photo[c][r]`.", "Reverse every row.", "Return the photo."],
                code={
                    "python": """
                        class Solution:
                            def rotateClockwise(self, photo: List[List[int]]) -> List[List[int]]:
                                n = len(photo)
                                for r in range(n):  #@transpose
                                    for c in range(r + 1, n):  #@transpose
                                        photo[r][c], photo[c][r] = photo[c][r], photo[r][c]  #@transpose
                                for row in photo:  #@reverse
                                    row.reverse()  #@reverse
                                return photo  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[][] rotateClockwise(int[][] photo) {
                                int n = photo.length;
                                for (int r = 0; r < n; r++)  //@transpose
                                    for (int c = r + 1; c < n; c++) {  //@transpose
                                        int t = photo[r][c]; photo[r][c] = photo[c][r]; photo[c][r] = t;  //@transpose
                                    }
                                for (int[] row : photo)  //@reverse
                                    for (int i = 0, j = n - 1; i < j; i++, j--) {  //@reverse
                                        int t = row[i]; row[i] = row[j]; row[j] = t;  //@reverse
                                    }
                                return photo;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<vector<int>> rotateClockwise(vector<vector<int>>& photo) {
                                int n = photo.size();
                                for (int r = 0; r < n; r++)  //@transpose
                                    for (int c = r + 1; c < n; c++) swap(photo[r][c], photo[c][r]);  //@transpose
                                for (auto& row : photo) reverse(row.begin(), row.end());  //@reverse
                                return photo;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int** rotateClockwise(int** photo, int photoSize, int* photoColSize, int* returnSize, int** returnColumnSizes) {
                            int n = photoSize;
                            for (int r = 0; r < n; r++)  //@transpose
                                for (int c = r + 1; c < n; c++) {  //@transpose
                                    int t = photo[r][c]; photo[r][c] = photo[c][r]; photo[c][r] = t;  //@transpose
                                }
                            for (int r = 0; r < n; r++)  //@reverse
                                for (int i = 0, j = n - 1; i < j; i++, j--) {  //@reverse
                                    int t = photo[r][i]; photo[r][i] = photo[r][j]; photo[r][j] = t;  //@reverse
                                }
                            *returnSize = n;  //@ret
                            *returnColumnSizes = malloc(n * sizeof(int));  //@ret
                            for (int i = 0; i < n; i++) (*returnColumnSizes)[i] = n;  //@ret
                            return photo;  //@ret
                        }
                    """,
                },
                lines=[
                    ("transpose", "Mirror over the main diagonal. Starting `c` at `r + 1` swaps each pair exactly once; including `c ≤ r` would undo the swaps."),
                    ("reverse", "Mirror each row left-to-right with two pointers meeting in the middle."),
                    ("ret", "Transpose then row-reverse = clockwise rotation, in place."),
                ],
                complexity=["**Time O(n²):** about n²/2 swaps for the transpose plus n²/2 for the reversals. **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - Clockwise 90°: **transpose, then reverse each row**. Counter-clockwise: transpose, then reverse each
              column (or reverse rows first, then transpose).
            - Break a complicated index map into simple, in-place-friendly steps.
            - When transposing in place, swap only above the diagonal.
            """
        ],
    )


@problem
def spiral_readout():
    g = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
    m, n = len(g), len(g[0])

    def spiral(grid):
        top, bottom, left, right = 0, len(grid) - 1, 0, len(grid[0]) - 1
        out = []
        while top <= bottom and left <= right:
            out += grid[top][left:right + 1]
            top += 1
            out += [grid[r][right] for r in range(top, bottom + 1)]
            right -= 1
            if top <= bottom:
                out += grid[bottom][left:right + 1][::-1]
                bottom -= 1
            if left <= right:
                out += [grid[r][left] for r in range(bottom, top - 1, -1)]
                left += 1
        return out

    want = spiral(g)

    w1 = Steps("Walk like a robot: go straight, and turn right when the next cell is outside or already visited.")
    seen = set()
    r = c = d = 0
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    names = ["right", "down", "left", "up"]
    order = []
    for k in range(m * n):
        order.append(g[r][c])
        seen.add((r, c))
        nr, nc = r + dirs[d][0], c + dirs[d][1]
        turned = False
        if not (0 <= nr < m and 0 <= nc < n) or (nr, nc) in seen:
            d = (d + 1) % 4
            nr, nc = r + dirs[d][0], c + dirs[d][1]
            turned = True
        if turned or k in (0, m * n - 1):
            w1.step(f"Read {g[r][c]} at ({r}, {c})." + (f" Blocked ahead, so turn {names[d]}." if turned and k < m * n - 1 else ""), Grid(g, st={p: "dim" for p in seen} | {(r, c): "active"}), Vars(output=str(order)))
        r, c = nr, nc
    w1.steps[-1]["result"] = str(want)

    w2 = Steps("Keep four borders. Read the top row, right column, bottom row, left column, shrinking the border after each.")
    top, bottom, left, right = 0, m - 1, 0, n - 1
    out = []
    while top <= bottom and left <= right:
        seg = g[top][left:right + 1]
        out += seg
        w2.step(f"Top row {top}, columns {left}…{right}: {seg}. Then top moves down.", Grid(g, st={(top, c): "active" for c in range(left, right + 1)}), Vars(top=top, bottom=bottom, left=left, right=right))
        top += 1
        seg = [g[rr][right] for rr in range(top, bottom + 1)]
        out += seg
        if seg:
            w2.step(f"Right column {right}, rows {top}…{bottom}: {seg}. Then right moves left.", Grid(g, st={(rr, right): "active" for rr in range(top, bottom + 1)}), Vars(top=top, bottom=bottom, left=left, right=right))
        right -= 1
        if top <= bottom:
            seg = g[bottom][left:right + 1][::-1]
            out += seg
            w2.step(f"Bottom row {bottom}, right to left: {seg}. Then bottom moves up.", Grid(g, st={(bottom, c): "active" for c in range(left, right + 1)}), Vars(top=top, bottom=bottom, left=left, right=right))
            bottom -= 1
        if left <= right:
            seg = [g[rr][left] for rr in range(bottom, top - 1, -1)]
            out += seg
            if seg:
                w2.step(f"Left column {left}, bottom to top: {seg}. Then left moves right.", Grid(g, st={(rr, left): "active" for rr in range(top, bottom + 1)}), Vars(top=top, bottom=bottom, left=left, right=right))
            left += 1
    w2.step(f"Borders crossed: done. {out}", Grid(g), result=out)

    sol(
        "spiral-readout",
        summary="""
            Track the four borders of the part not yet read. Each lap reads the top row, the right column, the bottom
            row (backwards) and the left column (upwards), moving each border inward right after its side is read.
            The only subtle part is stopping the bottom and left sides when a single row or column is left.
        """,
        question=[
            """
            Read all values clockwise in a spiral, starting at the top-left: right along the top, down the right
            side, left along the bottom, up the left side, then repeat on the inner part.

            - **The grid needn't be square.** A 3 × 4 grid's last lap is a single row; a 3 × 1 grid is read straight
              down.
            - **Every value exactly once.** Double-reading the middle row or column of a thin grid is the classic bug.
            - **Size:** up to 500 × 500.
            """
        ],
        think=[
            """
            Take the 3 × 4 grid numbered 1 to 12. Outer lap: top row 1, 2, 3, 4; right column 8, 12; bottom row
            backwards 11, 10, 9; left column upwards 5. Inner part: just the row 6, 7.
            """,
            fig(Grid(g, st={(0, c): "active" for c in range(4)} | {(1, 3): "found", (2, 3): "found"} | {(2, c): "mark" for c in range(3)} | {(1, 0): "new"}),
                caption="Outer lap: top, right, bottom (backwards), left (upwards). The cells 6 and 7 remain."),
            """
            After reading a side, that side is used up, so its border moves inward: after the top row, `top` goes
            down by one; after the right column, `right` goes left; and so on. The unread part is always the
            rectangle `top … bottom × left … right`.

            When the rectangle shrinks to **one row**, reading its top row uses it up completely, so there's no
            bottom row left to read backwards. The check `top <= bottom` before the bottom side (and `left <= right`
            before the left side) prevents reading the same cells twice.
            """,
        ],
        approaches=[
            approach(
                "Walk and turn, with a visited grid",
                "better",
                "O(m · n)",
                "O(m · n)",
                idea=["Simulate a walker: start at (0, 0) heading right. After reading a cell, if the next cell ahead is outside the grid or already visited, turn right (right → down → left → up). Mark visited cells in an m × n boolean grid. Stop after reading m · n cells."],
                walk=w1,
                build=["Directions in clockwise order: right, down, left, up.", "Repeat m · n times: read the cell, mark it visited.", "Look ahead; if blocked, turn clockwise.", "Step forward."],
                code={
                    "python": """
                        class Solution:
                            def spiralOrder(self, grid: List[List[int]]) -> List[int]:
                                m, n = len(grid), len(grid[0])
                                seen = [[False] * n for _ in range(m)]  #@seen
                                dr, dc = [0, 1, 0, -1], [1, 0, -1, 0]  #@dirs
                                r = c = d = 0  #@dirs
                                out = []
                                for _ in range(m * n):  #@read
                                    out.append(grid[r][c])  #@read
                                    seen[r][c] = True  #@read
                                    nr, nc = r + dr[d], c + dc[d]  #@turn
                                    if not (0 <= nr < m and 0 <= nc < n) or seen[nr][nc]:  #@turn
                                        d = (d + 1) % 4  #@turn
                                    r, c = r + dr[d], c + dc[d]  #@step
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] spiralOrder(int[][] grid) {
                                int m = grid.length, n = grid[0].length;
                                boolean[][] seen = new boolean[m][n];  //@seen
                                int[] dr = {0, 1, 0, -1}, dc = {1, 0, -1, 0};  //@dirs
                                int r = 0, c = 0, d = 0;  //@dirs
                                int[] out = new int[m * n];
                                for (int k = 0; k < m * n; k++) {  //@read
                                    out[k] = grid[r][c];  //@read
                                    seen[r][c] = true;  //@read
                                    int nr = r + dr[d], nc = c + dc[d];  //@turn
                                    if (nr < 0 || nr >= m || nc < 0 || nc >= n || seen[nr][nc]) d = (d + 1) % 4;  //@turn
                                    r += dr[d];  //@step
                                    c += dc[d];  //@step
                                }
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> spiralOrder(vector<vector<int>>& grid) {
                                int m = grid.size(), n = grid[0].size();
                                vector<vector<bool>> seen(m, vector<bool>(n, false));  //@seen
                                int dr[] = {0, 1, 0, -1}, dc[] = {1, 0, -1, 0};  //@dirs
                                int r = 0, c = 0, d = 0;  //@dirs
                                vector<int> out;
                                for (int k = 0; k < m * n; k++) {  //@read
                                    out.push_back(grid[r][c]);  //@read
                                    seen[r][c] = true;  //@read
                                    int nr = r + dr[d], nc = c + dc[d];  //@turn
                                    if (nr < 0 || nr >= m || nc < 0 || nc >= n || seen[nr][nc]) d = (d + 1) % 4;  //@turn
                                    r += dr[d];  //@step
                                    c += dc[d];  //@step
                                }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* spiralOrder(int** grid, int gridSize, int* gridColSize, int* returnSize) {
                            int m = gridSize, n = gridColSize[0];
                            bool* seen = calloc(m * n, sizeof(bool));  //@seen
                            int dr[] = {0, 1, 0, -1}, dc[] = {1, 0, -1, 0};  //@dirs
                            int r = 0, c = 0, d = 0;  //@dirs
                            int* out = malloc(m * n * sizeof(int));
                            for (int k = 0; k < m * n; k++) {  //@read
                                out[k] = grid[r][c];  //@read
                                seen[r * n + c] = true;  //@read
                                int nr = r + dr[d], nc = c + dc[d];  //@turn
                                if (nr < 0 || nr >= m || nc < 0 || nc >= n || seen[nr * n + nc]) d = (d + 1) % 4;  //@turn
                                r += dr[d];  //@step
                                c += dc[d];  //@step
                            }
                            free(seen);  //@ret
                            *returnSize = m * n;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("seen", "Which cells have been read, so the walker knows when to turn.", {"c": "One flat array; cell (r, c) is at `r * n + c`."}),
                    ("dirs", "Row and column steps for right, down, left, up: clockwise order, so `d + 1` is always a right turn."),
                    ("read", "Read the current cell and mark it."),
                    ("turn", "If the cell ahead is off the grid or already read, turn clockwise. One turn is always enough while unread cells remain."),
                    ("step", "Move one cell in the current direction. After the very last read the walker may step off the grid, but the loop ends before reading again."),
                    ("ret", "All m · n values in spiral order.", {"c": "Free the marks; report the length."}),
                ],
                complexity=["**Time O(m · n).** **Space O(m · n)** for the visited grid."],
                limits=["The visited grid only answers \"where does the unread part end?\", and that's always a rectangle described by four numbers."],
            ),
            approach(
                "Shrinking borders",
                "best",
                "O(m · n)",
                "O(1)",
                idea=[
                    """
                    Keep `top`, `bottom`, `left`, `right` around the unread rectangle. While it's non-empty:

                    1. read row `top` from `left` to `right`, then `top += 1`;
                    2. read column `right` from `top` to `bottom`, then `right −= 1`;
                    3. if `top ≤ bottom`, read row `bottom` from `right` down to `left`, then `bottom −= 1`;
                    4. if `left ≤ right`, read column `left` from `bottom` up to `top`, then `left += 1`.

                    Checks 3 and 4 matter when only one row or one column remains: steps 1 and 2 already used it up.
                    """
                ],
                walk=w2,
                build=["Set the four borders to the grid's edges.", "Loop while `top ≤ bottom` and `left ≤ right`, doing the four sides in order and moving each border after its side.", "Guard the bottom and left sides with `top ≤ bottom` and `left ≤ right`."],
                code={
                    "python": """
                        class Solution:
                            def spiralOrder(self, grid: List[List[int]]) -> List[int]:
                                top, bottom, left, right = 0, len(grid) - 1, 0, len(grid[0]) - 1  #@borders
                                out = []
                                while top <= bottom and left <= right:  #@loop
                                    for c in range(left, right + 1):  #@top
                                        out.append(grid[top][c])  #@top
                                    top += 1  #@top
                                    for r in range(top, bottom + 1):  #@right
                                        out.append(grid[r][right])  #@right
                                    right -= 1  #@right
                                    if top <= bottom:  #@bottom
                                        for c in range(right, left - 1, -1):  #@bottom
                                            out.append(grid[bottom][c])  #@bottom
                                        bottom -= 1  #@bottom
                                    if left <= right:  #@left
                                        for r in range(bottom, top - 1, -1):  #@left
                                            out.append(grid[r][left])  #@left
                                        left += 1  #@left
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[] spiralOrder(int[][] grid) {
                                int m = grid.length, n = grid[0].length;
                                int top = 0, bottom = m - 1, left = 0, right = n - 1;  //@borders
                                int[] out = new int[m * n];
                                int k = 0;
                                while (top <= bottom && left <= right) {  //@loop
                                    for (int c = left; c <= right; c++) out[k++] = grid[top][c];  //@top
                                    top++;  //@top
                                    for (int r = top; r <= bottom; r++) out[k++] = grid[r][right];  //@right
                                    right--;  //@right
                                    if (top <= bottom) {  //@bottom
                                        for (int c = right; c >= left; c--) out[k++] = grid[bottom][c];  //@bottom
                                        bottom--;  //@bottom
                                    }
                                    if (left <= right) {  //@left
                                        for (int r = bottom; r >= top; r--) out[k++] = grid[r][left];  //@left
                                        left++;  //@left
                                    }
                                }
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<int> spiralOrder(vector<vector<int>>& grid) {
                                int top = 0, bottom = grid.size() - 1, left = 0, right = grid[0].size() - 1;  //@borders
                                vector<int> out;
                                while (top <= bottom && left <= right) {  //@loop
                                    for (int c = left; c <= right; c++) out.push_back(grid[top][c]);  //@top
                                    top++;  //@top
                                    for (int r = top; r <= bottom; r++) out.push_back(grid[r][right]);  //@right
                                    right--;  //@right
                                    if (top <= bottom) {  //@bottom
                                        for (int c = right; c >= left; c--) out.push_back(grid[bottom][c]);  //@bottom
                                        bottom--;  //@bottom
                                    }
                                    if (left <= right) {  //@left
                                        for (int r = bottom; r >= top; r--) out.push_back(grid[r][left]);  //@left
                                        left++;  //@left
                                    }
                                }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int* spiralOrder(int** grid, int gridSize, int* gridColSize, int* returnSize) {
                            int m = gridSize, n = gridColSize[0];
                            int top = 0, bottom = m - 1, left = 0, right = n - 1;  //@borders
                            int* out = malloc(m * n * sizeof(int));
                            int k = 0;
                            while (top <= bottom && left <= right) {  //@loop
                                for (int c = left; c <= right; c++) out[k++] = grid[top][c];  //@top
                                top++;  //@top
                                for (int r = top; r <= bottom; r++) out[k++] = grid[r][right];  //@right
                                right--;  //@right
                                if (top <= bottom) {  //@bottom
                                    for (int c = right; c >= left; c--) out[k++] = grid[bottom][c];  //@bottom
                                    bottom--;  //@bottom
                                }
                                if (left <= right) {  //@left
                                    for (int r = bottom; r >= top; r--) out[k++] = grid[r][left];  //@left
                                    left++;  //@left
                                }
                            }
                            *returnSize = k;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("borders", "The unread rectangle starts as the whole grid."),
                    ("loop", "Keep going while the rectangle has at least one cell."),
                    ("top", "Top row, left to right; then that row is used up."),
                    ("right", "Right column, from the new top down; then that column is used up."),
                    ("bottom", "Bottom row, right to left, only if a row is still left (a single-row rectangle was fully read by the top step)."),
                    ("left", "Left column, bottom to top, only if a column is still left."),
                    ("ret", "Every value read once.", {"c": "`k` counted the values written: m · n."}),
                ],
                complexity=["**Time O(m · n).** **Space O(1)** besides the output."],
            ),
        ],
        takeaways=[
            """
            - For layer-by-layer grid walks, keep **four borders** and shrink the one you just consumed.
            - Re-check the borders before the third and fourth sides; thin rectangles break naive loops.
            - The "walk and turn when blocked" simulation is a general fallback for any path that hugs walls.
            """
        ],
    )
