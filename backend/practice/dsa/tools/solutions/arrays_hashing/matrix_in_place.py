"""Arrays & Hashing: matrix in place."""
from sol import Grid, Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


def life(b):
    m, n = len(b), len(b[0])
    out = [[0] * n for _ in range(m)]
    for r in range(m):
        for c in range(n):
            k = sum(b[rr][cc] for rr in range(max(0, r - 1), min(m, r + 2)) for cc in range(max(0, c - 1), min(n, c + 2))) - b[r][c]
            out[r][c] = 1 if k == 3 or (k == 2 and b[r][c]) else 0
    return out


def nbrs(b, r, c):
    m, n = len(b), len(b[0])
    return [(rr, cc) for rr in range(max(0, r - 1), min(m, r + 2)) for cc in range(max(0, c - 1), min(n, c + 2)) if (rr, cc) != (r, c)]


@problem
def colony_next_generation():
    board = [[0, 1, 0, 0], [0, 0, 1, 0], [1, 1, 1, 0], [0, 0, 0, 0]]
    nxt = life(board)
    m, n = len(board), len(board[0])

    w1 = Steps("Read neighbours from an untouched copy; write the next generation into the board.")
    w1.step("Copy the board. Every count below reads the copy, so updates never disturb later counts.", Grid(board, label="copy (generation 0)"))
    shown = [(0, 1), (1, 0), (1, 2), (2, 1), (3, 1), (2, 2)]
    for r, c in shown:
        k = sum(board[a][b] for a, b in nbrs(board, r, c))
        rule = ("alive with " + str(k) + (" → stays" if k in (2, 3) else " → dies")) if board[r][c] else ("empty with " + str(k) + (" → born" if k == 3 else " → stays empty"))
        st = {p: "mark" for p in nbrs(board, r, c) if board[p[0]][p[1]]}
        st[(r, c)] = "active"
        w1.step(f"Cell ({r}, {c}): {rule}.", Grid(board, st=st, label="copy (generation 0)"))
    w1.step("All cells done the same way.", Grid(nxt, st={(r, c): "new" for r in range(m) for c in range(n) if nxt[r][c] != board[r][c]}, label="generation 1 (changed cells shaded)"), result=nxt)

    w2 = Steps("Keep the old state in bit 0 and write the new state into bit 1 of the same cell. Shift right at the end.")
    g = [row[:] for row in board]
    w2.step("Each cell is 0 or 1 now: bit 0 is 'alive this generation'. Bit 1 is free to hold next generation.", Grid(g, label="cell values"))
    for r in range(m):
        for c in range(n):
            k = sum(g[a][b] & 1 for a, b in nbrs(g, r, c))
            if k == 3 or (k == 2 and g[r][c] & 1):
                g[r][c] |= 2
    w2.step("First pass: count neighbours with `value & 1` (the old state, even in cells already updated) and set bit 1 (add 2) where the cell lives next. 3 = alive now and next; 2 = born; 1 = dies; 0 = stays empty.", Grid(g, st={(r, c): "new" for r in range(m) for c in range(n) if g[r][c] & 2}, label="old in bit 0, new in bit 1"))
    w2.step("Second pass: shift every cell right by one bit, keeping only the new state.", Grid([[x >> 1 for x in row] for row in g], label="generation 1"), result=nxt)

    sol(
        "colony-next-generation",
        summary="""
            Every cell must be updated from the **old** board, so naively writing new values would corrupt the
            neighbour counts of cells not yet visited. Either read from a copy (O(mn) extra space), or store the new
            state in a spare bit of each cell, leaving the old state readable until a final pass shifts it out
            (O(1) extra space).
        """,
        question=[
            """
            Apply one generation of the rules to a grid of 0s (empty) and 1s (alive). Each cell looks at its up to 8
            neighbours (including diagonals):

            - **Alive** with 2 or 3 living neighbours: stays alive. Fewer than 2 or more than 3: dies.
            - **Empty** with exactly 3 living neighbours: becomes alive.

            - **All cells change at the same moment**, based on the old board. This is the whole difficulty.
            - **Edges and corners** simply have fewer neighbours (5 or 3); nothing wraps around.
            - **Size:** up to 200 × 200, so the work is tiny; the interesting constraint is "without a second grid".
            """
        ],
        think=[
            """
            Take this 4 × 4 board. Cell (2, 1) is alive with 3 living neighbours, so it survives; cell (1, 0) is empty
            with 3 living neighbours, so it's born.
            """,
            fig(Grid(board, label="now"), Grid(nxt, label="one generation later")),
            """
            Now try updating **in place**, row by row. When you reach cell (1, 0) you'll count its neighbours, but
            row 0 has already been rewritten: (0, 1) just died, so you'd count 2 instead of 3 and wrongly leave
            (1, 0) empty. Each cell's new value must come from neighbours' **old** values.

            Two ways to keep the old values available:

            1. Read from a **copy** of the board.
            2. Keep both values **in the same cell**. Cells are 0 or 1, so only bit 0 is used. Put the next state in
               bit 1: old = `value & 1`, new = `value >> 1`. Counting with `& 1` always sees the old state, whether
               or not a neighbour has been updated yet.
            """,
        ],
        approaches=[
            approach(
                "Count from a copy of the board",
                "better",
                "O(m · n)",
                "O(m · n)",
                idea=["Copy the board. For every cell, count living neighbours **in the copy** and write the new state into the board (or a new grid). The copy never changes, so every count sees the old generation."],
                walk=w1,
                build=["Copy the board.", "For each cell, sum the copy's values in the 3 × 3 block around it (clipped to the edges), minus the cell itself.", "Apply the rules and write the result.", "Return the result."],
                code={
                    "python": """
                        class Solution:
                            def nextGeneration(self, board: List[List[int]]) -> List[List[int]]:
                                old = [row[:] for row in board]  #@copy
                                m, n = len(old), len(old[0])
                                for r in range(m):  #@cells
                                    for c in range(n):  #@cells
                                        live = 0  #@count
                                        for rr in range(max(0, r - 1), min(m, r + 2)):  #@count
                                            for cc in range(max(0, c - 1), min(n, c + 2)):  #@count
                                                live += old[rr][cc]  #@count
                                        live -= old[r][c]  #@count
                                        board[r][c] = 1 if live == 3 or (live == 2 and old[r][c]) else 0  #@rule
                                return board  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[][] nextGeneration(int[][] board) {
                                int m = board.length, n = board[0].length;
                                int[][] old = new int[m][];  //@copy
                                for (int r = 0; r < m; r++) old[r] = board[r].clone();  //@copy
                                for (int r = 0; r < m; r++) {  //@cells
                                    for (int c = 0; c < n; c++) {  //@cells
                                        int live = 0;  //@count
                                        for (int rr = Math.max(0, r - 1); rr <= Math.min(m - 1, r + 1); rr++)  //@count
                                            for (int cc = Math.max(0, c - 1); cc <= Math.min(n - 1, c + 1); cc++)  //@count
                                                live += old[rr][cc];  //@count
                                        live -= old[r][c];  //@count
                                        board[r][c] = (live == 3 || (live == 2 && old[r][c] == 1)) ? 1 : 0;  //@rule
                                    }
                                }
                                return board;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<vector<int>> nextGeneration(vector<vector<int>>& board) {
                                int m = board.size(), n = board[0].size();
                                vector<vector<int>> old = board;  //@copy
                                for (int r = 0; r < m; r++) {  //@cells
                                    for (int c = 0; c < n; c++) {  //@cells
                                        int live = 0;  //@count
                                        for (int rr = max(0, r - 1); rr <= min(m - 1, r + 1); rr++)  //@count
                                            for (int cc = max(0, c - 1); cc <= min(n - 1, c + 1); cc++)  //@count
                                                live += old[rr][cc];  //@count
                                        live -= old[r][c];  //@count
                                        board[r][c] = (live == 3 || (live == 2 && old[r][c] == 1)) ? 1 : 0;  //@rule
                                    }
                                }
                                return board;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int** nextGeneration(int** board, int boardSize, int* boardColSize, int* returnSize, int** returnColumnSizes) {
                            int m = boardSize, n = boardColSize[0];
                            int** out = malloc(m * sizeof(int*));  //@copy
                            for (int r = 0; r < m; r++) out[r] = malloc(n * sizeof(int));  //@copy
                            for (int r = 0; r < m; r++) {  //@cells
                                for (int c = 0; c < n; c++) {  //@cells
                                    int live = 0;  //@count
                                    for (int rr = r > 0 ? r - 1 : 0; rr <= (r + 1 < m ? r + 1 : m - 1); rr++)  //@count
                                        for (int cc = c > 0 ? c - 1 : 0; cc <= (c + 1 < n ? c + 1 : n - 1); cc++)  //@count
                                            live += board[rr][cc];  //@count
                                    live -= board[r][c];  //@count
                                    out[r][c] = (live == 3 || (live == 2 && board[r][c] == 1)) ? 1 : 0;  //@rule
                                }
                            }
                            *returnSize = m;  //@ret
                            *returnColumnSizes = malloc(m * sizeof(int));  //@ret
                            for (int r = 0; r < m; r++) (*returnColumnSizes)[r] = n;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("copy", "A frozen snapshot of the current generation. All reading happens here.", {"c": "Here the input stays untouched and serves as the snapshot; the next generation is written into a fresh grid."}),
                    ("cells", "Every cell gets its new state."),
                    ("count", "Sum the 3 × 3 block around the cell, clipped at the borders (`max(0, …)` / `min(…, last)`), then subtract the cell itself: what's left is its living neighbours."),
                    ("rule", "Alive next if it has exactly 3 neighbours, or 2 and is alive now. Every other case is empty."),
                    ("ret", "The next generation.", {"c": "Report the row count and every row's length; the caller frees the new grid."}),
                ],
                complexity=["**Time O(m · n):** at most 9 reads per cell. **Space O(m · n)** for the copy."],
                limits=["The copy doubles the memory. Each cell only uses one of its 32 bits, so the next state can be stored alongside the current one instead."],
            ),
            approach(
                "Two states in one cell (bit tricks)",
                "best",
                "O(m · n)",
                "O(1)",
                idea=[
                    """
                    Use bit 0 for the current state and bit 1 for the next state.

                    - **Pass 1:** for each cell, count neighbours using `value & 1` (the current state, whether or not
                      that neighbour has been processed). If the cell lives in the next generation, set bit 1
                      (`value |= 2`). Bit 0 is never touched, so later counts stay correct.
                    - **Pass 2:** shift every cell right by one (`value >>= 1`), so bit 1 becomes the new value.
                    """
                ],
                walk=w2,
                build=["For each cell, count neighbours with `board[rr][cc] & 1`.", "If `live == 3`, or `live == 2` and the cell is alive (`& 1`), do `board[r][c] |= 2`.", "Afterwards, `board[r][c] >>= 1` for every cell.", "Return the board."],
                code={
                    "python": """
                        class Solution:
                            def nextGeneration(self, board: List[List[int]]) -> List[List[int]]:
                                m, n = len(board), len(board[0])
                                for r in range(m):  #@cells
                                    for c in range(n):  #@cells
                                        live = 0  #@count
                                        for rr in range(max(0, r - 1), min(m, r + 2)):  #@count
                                            for cc in range(max(0, c - 1), min(n, c + 2)):  #@count
                                                live += board[rr][cc] & 1  #@count
                                        live -= board[r][c] & 1  #@count
                                        if live == 3 or (live == 2 and board[r][c] & 1):  #@mark
                                            board[r][c] |= 2  #@mark
                                for row in board:  #@shift
                                    for c in range(n):  #@shift
                                        row[c] >>= 1  #@shift
                                return board  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[][] nextGeneration(int[][] board) {
                                int m = board.length, n = board[0].length;
                                for (int r = 0; r < m; r++) {  //@cells
                                    for (int c = 0; c < n; c++) {  //@cells
                                        int live = 0;  //@count
                                        for (int rr = Math.max(0, r - 1); rr <= Math.min(m - 1, r + 1); rr++)  //@count
                                            for (int cc = Math.max(0, c - 1); cc <= Math.min(n - 1, c + 1); cc++)  //@count
                                                live += board[rr][cc] & 1;  //@count
                                        live -= board[r][c] & 1;  //@count
                                        if (live == 3 || (live == 2 && (board[r][c] & 1) == 1)) board[r][c] |= 2;  //@mark
                                    }
                                }
                                for (int[] row : board)  //@shift
                                    for (int c = 0; c < n; c++) row[c] >>= 1;  //@shift
                                return board;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<vector<int>> nextGeneration(vector<vector<int>>& board) {
                                int m = board.size(), n = board[0].size();
                                for (int r = 0; r < m; r++) {  //@cells
                                    for (int c = 0; c < n; c++) {  //@cells
                                        int live = 0;  //@count
                                        for (int rr = max(0, r - 1); rr <= min(m - 1, r + 1); rr++)  //@count
                                            for (int cc = max(0, c - 1); cc <= min(n - 1, c + 1); cc++)  //@count
                                                live += board[rr][cc] & 1;  //@count
                                        live -= board[r][c] & 1;  //@count
                                        if (live == 3 || (live == 2 && (board[r][c] & 1))) board[r][c] |= 2;  //@mark
                                    }
                                }
                                for (auto& row : board)  //@shift
                                    for (int& x : row) x >>= 1;  //@shift
                                return board;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int** nextGeneration(int** board, int boardSize, int* boardColSize, int* returnSize, int** returnColumnSizes) {
                            int m = boardSize, n = boardColSize[0];
                            for (int r = 0; r < m; r++) {  //@cells
                                for (int c = 0; c < n; c++) {  //@cells
                                    int live = 0;  //@count
                                    for (int rr = r > 0 ? r - 1 : 0; rr <= (r + 1 < m ? r + 1 : m - 1); rr++)  //@count
                                        for (int cc = c > 0 ? c - 1 : 0; cc <= (c + 1 < n ? c + 1 : n - 1); cc++)  //@count
                                            live += board[rr][cc] & 1;  //@count
                                    live -= board[r][c] & 1;  //@count
                                    if (live == 3 || (live == 2 && (board[r][c] & 1))) board[r][c] |= 2;  //@mark
                                }
                            }
                            for (int r = 0; r < m; r++)  //@shift
                                for (int c = 0; c < n; c++) board[r][c] >>= 1;  //@shift
                            *returnSize = m;  //@ret
                            *returnColumnSizes = malloc(m * sizeof(int));  //@ret
                            for (int r = 0; r < m; r++) (*returnColumnSizes)[r] = n;  //@ret
                            return board;  //@ret
                        }
                    """,
                },
                lines=[
                    ("cells", "Visit every cell once in the first pass."),
                    ("count", "`& 1` keeps only bit 0, the **current** generation, so a neighbour that already has its next state stored in bit 1 still counts correctly."),
                    ("mark", "If the cell lives next generation, set bit 1 (`|= 2`). Bit 0 is untouched, so other cells still read this cell's old state."),
                    ("shift", "Second pass: drop bit 0 and move bit 1 down. Every cell now holds just the new state."),
                    ("ret", "The board, updated in place.", {"c": "The grid is the input itself; only the column-size array is new."}),
                ],
                complexity=["**Time O(m · n):** two passes, at most 9 reads per cell. **Space O(1)** extra."],
            ),
        ],
        takeaways=[
            """
            - "Update everything simultaneously" means **read old, write new**. If you write in place, make sure
              unprocessed cells can still see old values.
            - Small values leave spare bits: store the next state in a higher bit, then shift.
            - Clip neighbour ranges with `max(0, r − 1)` / `min(m − 1, r + 1)` instead of special-casing borders.
            """
        ],
    )


@problem
def soften_the_photo():
    img = [[10, 20, 30], [40, 250, 60], [70, 80, 90]]
    m, n = len(img), len(img[0])

    def soft(g):
        out = []
        for r in range(m):
            row = []
            for c in range(n):
                vals = [g[a][b] for a in range(max(0, r - 1), min(m, r + 2)) for b in range(max(0, c - 1), min(n, c + 2))]
                row.append(sum(vals) // len(vals))
            out.append(row)
        return out

    res = soft(img)

    w1 = Steps("Average each pixel's 3 × 3 block in the original photo, clipped at the edges.")
    for r, c in [(0, 0), (0, 1), (1, 1), (2, 2)]:
        blk = [(a, b) for a in range(max(0, r - 1), min(m, r + 2)) for b in range(max(0, c - 1), min(n, c + 2))]
        tot = sum(img[a][b] for a, b in blk)
        st = {p: "mark" for p in blk}
        st[(r, c)] = "active"
        w1.step(f"Pixel ({r}, {c}): {len(blk)} pixels in its block sum to {tot}; {tot} // {len(blk)} = {tot // len(blk)}.", Grid(img, st=st, label="original"))
    w1.step("Every pixel computed from the original values.", Grid(res, label="softened"), result=res)

    w2 = Steps("Pixels use 8 bits (0 … 255). Store each new value in bits 8 … 15 of the same cell; shift down at the end.")
    g = [row[:] for row in img]
    for r in range(m):
        for c in range(n):
            vals = [g[a][b] & 255 for a in range(max(0, r - 1), min(m, r + 2)) for b in range(max(0, c - 1), min(n, c + 2))]
            g[r][c] |= (sum(vals) // len(vals)) << 8
    w2.step("Pass 1: every average is computed from `value & 255` (the original 8 bits) and stored as `avg << 8`, i.e. avg × 256 added on top.", Grid(g, label="new × 256 + old"))
    w2.step("Pass 2: shift every cell right by 8 bits, leaving only the new value.", Grid([[x >> 8 for x in row] for row in g], label="softened"), result=res)

    sol(
        "soften-the-photo",
        summary="""
            Each pixel becomes the rounded-down average of the in-bounds pixels of its 3 × 3 block, all computed from
            the **original** photo. Reading from a copy is simplest; to avoid the copy, store each new value in the
            unused high bits of its cell and shift them down at the end.
        """,
        question=[
            """
            Replace every pixel by the average (rounded down) of the pixels in the 3 × 3 block centred on it,
            counting only pixels inside the photo.

            - **Different pixels average different counts:** a corner averages 4 pixels, an edge pixel 6, an inner
              pixel 9. A 1 × 1 photo averages just itself.
            - **All averages use the original values**, never already-softened neighbours.
            - **Rounded down:** integer division.
            - **Values 0 … 255** fit in 8 bits, leaving plenty of spare bits in an `int`.
            """
        ],
        think=[
            """
            Take a 3 × 3 photo with a bright centre (250). The centre averages all 9 pixels: 650 / 9 → 72. The corner
            (0, 0) averages only its 4-pixel block: 10 + 20 + 40 + 250 = 320, 320 / 4 = 80.
            """,
            fig(Grid(img, st={(0, 0): "active", (0, 1): "mark", (1, 0): "mark", (1, 1): "mark"}, label="original"), Grid(res, st={(0, 0): "answer"}, label="softened"),
                caption="The corner's block has 4 pixels; the centre's has 9."),
            """
            If you overwrote pixels as you go, the next pixel's block would include a softened value, which is
            wrong. So, as with any "simultaneous" grid update, either read from a copy, or keep the original value
            recoverable inside the cell (`value & 255`) while the new one sits in higher bits (`value >> 8`).
            """,
        ],
        approaches=[
            approach(
                "Average from a copy",
                "better",
                "O(m · n)",
                "O(m · n)",
                idea=["Keep the original photo untouched and write each average into a new grid. For every pixel, add up the in-bounds block and divide by how many pixels it had."],
                walk=w1,
                build=["Make an output grid.", "For each pixel, sum the original values in rows r−1 … r+1 and columns c−1 … c+1 that are inside the photo, counting them.", "Store `sum // count`.", "Return the output grid."],
                code={
                    "python": """
                        class Solution:
                            def soften(self, image: List[List[int]]) -> List[List[int]]:
                                m, n = len(image), len(image[0])
                                out = [[0] * n for _ in range(m)]  #@out
                                for r in range(m):  #@cells
                                    for c in range(n):  #@cells
                                        total = count = 0  #@block
                                        for rr in range(max(0, r - 1), min(m, r + 2)):  #@block
                                            for cc in range(max(0, c - 1), min(n, c + 2)):  #@block
                                                total += image[rr][cc]  #@block
                                                count += 1  #@block
                                        out[r][c] = total // count  #@avg
                                return out  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[][] soften(int[][] image) {
                                int m = image.length, n = image[0].length;
                                int[][] out = new int[m][n];  //@out
                                for (int r = 0; r < m; r++) {  //@cells
                                    for (int c = 0; c < n; c++) {  //@cells
                                        int total = 0, count = 0;  //@block
                                        for (int rr = Math.max(0, r - 1); rr <= Math.min(m - 1, r + 1); rr++)  //@block
                                            for (int cc = Math.max(0, c - 1); cc <= Math.min(n - 1, c + 1); cc++) {  //@block
                                                total += image[rr][cc];  //@block
                                                count++;  //@block
                                            }  //@block
                                        out[r][c] = total / count;  //@avg
                                    }
                                }
                                return out;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<vector<int>> soften(vector<vector<int>>& image) {
                                int m = image.size(), n = image[0].size();
                                vector<vector<int>> out(m, vector<int>(n));  //@out
                                for (int r = 0; r < m; r++) {  //@cells
                                    for (int c = 0; c < n; c++) {  //@cells
                                        int total = 0, count = 0;  //@block
                                        for (int rr = max(0, r - 1); rr <= min(m - 1, r + 1); rr++)  //@block
                                            for (int cc = max(0, c - 1); cc <= min(n - 1, c + 1); cc++) {  //@block
                                                total += image[rr][cc];  //@block
                                                count++;  //@block
                                            }  //@block
                                        out[r][c] = total / count;  //@avg
                                    }
                                }
                                return out;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int** soften(int** image, int imageSize, int* imageColSize, int* returnSize, int** returnColumnSizes) {
                            int m = imageSize, n = imageColSize[0];
                            int** out = malloc(m * sizeof(int*));  //@out
                            for (int r = 0; r < m; r++) out[r] = malloc(n * sizeof(int));  //@out
                            for (int r = 0; r < m; r++) {  //@cells
                                for (int c = 0; c < n; c++) {  //@cells
                                    int total = 0, count = 0;  //@block
                                    for (int rr = r > 0 ? r - 1 : 0; rr <= (r + 1 < m ? r + 1 : m - 1); rr++)  //@block
                                        for (int cc = c > 0 ? c - 1 : 0; cc <= (c + 1 < n ? c + 1 : n - 1); cc++) {  //@block
                                            total += image[rr][cc];  //@block
                                            count++;  //@block
                                        }  //@block
                                    out[r][c] = total / count;  //@avg
                                }
                            }
                            *returnSize = m;  //@ret
                            *returnColumnSizes = malloc(m * sizeof(int));  //@ret
                            for (int r = 0; r < m; r++) (*returnColumnSizes)[r] = n;  //@ret
                            return out;  //@ret
                        }
                    """,
                },
                lines=[
                    ("out", "A fresh grid for the results, so the original stays readable."),
                    ("cells", "Every pixel."),
                    ("block", "Add up the 3 × 3 block clipped to the photo, and count how many pixels it really has (4, 6 or 9; fewer for very thin photos)."),
                    ("avg", "Integer division rounds down, as required."),
                    ("ret", "The softened photo.", {"c": "Report the row count and each row's length."}),
                ],
                complexity=["**Time O(m · n):** at most 9 reads per pixel. **Space O(m · n)** for the output grid."],
                limits=["A whole second grid, while each pixel uses only 8 of its cell's 32 bits. The new value fits in the spare bits."],
            ),
            approach(
                "Pack the new value into the high bits",
                "best",
                "O(m · n)",
                "O(1)",
                idea=[
                    """
                    A pixel value fits in bits 0 … 7. During one pass, read neighbours as `value & 255` (only the
                    original bits) and store each average in bits 8 … 15 with `value |= avg << 8`. Reads never see
                    the stored averages. A second pass `value >>= 8` keeps only the new values.
                    """
                ],
                walk=w2,
                build=["For each pixel, sum `image[rr][cc] & 255` over its clipped block, and count the pixels.", "`image[r][c] |= (total / count) << 8`.", "Afterwards shift every cell right by 8.", "Return the image."],
                code={
                    "python": """
                        class Solution:
                            def soften(self, image: List[List[int]]) -> List[List[int]]:
                                m, n = len(image), len(image[0])
                                for r in range(m):  #@cells
                                    for c in range(n):  #@cells
                                        total = count = 0  #@block
                                        for rr in range(max(0, r - 1), min(m, r + 2)):  #@block
                                            for cc in range(max(0, c - 1), min(n, c + 2)):  #@block
                                                total += image[rr][cc] & 255  #@block
                                                count += 1  #@block
                                        image[r][c] |= (total // count) << 8  #@pack
                                for row in image:  #@shift
                                    for c in range(n):  #@shift
                                        row[c] >>= 8  #@shift
                                return image  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int[][] soften(int[][] image) {
                                int m = image.length, n = image[0].length;
                                for (int r = 0; r < m; r++) {  //@cells
                                    for (int c = 0; c < n; c++) {  //@cells
                                        int total = 0, count = 0;  //@block
                                        for (int rr = Math.max(0, r - 1); rr <= Math.min(m - 1, r + 1); rr++)  //@block
                                            for (int cc = Math.max(0, c - 1); cc <= Math.min(n - 1, c + 1); cc++) {  //@block
                                                total += image[rr][cc] & 255;  //@block
                                                count++;  //@block
                                            }  //@block
                                        image[r][c] |= (total / count) << 8;  //@pack
                                    }
                                }
                                for (int[] row : image)  //@shift
                                    for (int c = 0; c < n; c++) row[c] >>= 8;  //@shift
                                return image;  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            vector<vector<int>> soften(vector<vector<int>>& image) {
                                int m = image.size(), n = image[0].size();
                                for (int r = 0; r < m; r++) {  //@cells
                                    for (int c = 0; c < n; c++) {  //@cells
                                        int total = 0, count = 0;  //@block
                                        for (int rr = max(0, r - 1); rr <= min(m - 1, r + 1); rr++)  //@block
                                            for (int cc = max(0, c - 1); cc <= min(n - 1, c + 1); cc++) {  //@block
                                                total += image[rr][cc] & 255;  //@block
                                                count++;  //@block
                                            }  //@block
                                        image[r][c] |= (total / count) << 8;  //@pack
                                    }
                                }
                                for (auto& row : image)  //@shift
                                    for (int& x : row) x >>= 8;  //@shift
                                return image;  //@ret
                            }
                        };
                    """,
                    "c": """
                        int** soften(int** image, int imageSize, int* imageColSize, int* returnSize, int** returnColumnSizes) {
                            int m = imageSize, n = imageColSize[0];
                            for (int r = 0; r < m; r++) {  //@cells
                                for (int c = 0; c < n; c++) {  //@cells
                                    int total = 0, count = 0;  //@block
                                    for (int rr = r > 0 ? r - 1 : 0; rr <= (r + 1 < m ? r + 1 : m - 1); rr++)  //@block
                                        for (int cc = c > 0 ? c - 1 : 0; cc <= (c + 1 < n ? c + 1 : n - 1); cc++) {  //@block
                                            total += image[rr][cc] & 255;  //@block
                                            count++;  //@block
                                        }  //@block
                                    image[r][c] |= (total / count) << 8;  //@pack
                                }
                            }
                            for (int r = 0; r < m; r++)  //@shift
                                for (int c = 0; c < n; c++) image[r][c] >>= 8;  //@shift
                            *returnSize = m;  //@ret
                            *returnColumnSizes = malloc(m * sizeof(int));  //@ret
                            for (int r = 0; r < m; r++) (*returnColumnSizes)[r] = n;  //@ret
                            return image;  //@ret
                        }
                    """,
                },
                lines=[
                    ("cells", "One pass over the pixels."),
                    ("block", "`& 255` keeps only the low 8 bits: the **original** pixel, even for neighbours that already carry their new value above."),
                    ("pack", "Store the average (also 0 … 255) in bits 8 … 15. The low 8 bits are left alone for pixels still to come."),
                    ("shift", "Drop the old 8 bits; the new value moves down into place."),
                    ("ret", "The softened photo, in place.", {"c": "Only the column-size array is new memory."}),
                ],
                complexity=["**Time O(m · n).** **Space O(1)** extra."],
            ),
        ],
        takeaways=[
            """
            - Simultaneous grid updates: read old, write new. A copy is easiest; packing old and new into one cell
              saves the memory.
            - `& mask` reads the old bits, `<< k` stores the new value above them, `>> k` finishes the job.
            - At borders, count how many cells you actually averaged; don't divide by 9 blindly.
            """
        ],
    )
