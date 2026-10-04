"""Lesson: In-place grid markers (Arrays & Hashing, pattern 15)."""
from lesson import Grid, M, Steps, code, fig, key, lesson, py, quiz, table, walk

# ---------------------------------------------------------------- the code

ZERO = {
    "python": """
        def set_zeroes(g):
            m, n = len(g), len(g[0])                                #@size
            row0 = any(g[0][c] == 0 for c in range(n))              #@flags
            col0 = any(g[r][0] == 0 for r in range(m))              #@flags
            for r in range(1, m):                                   #@mark
                for c in range(1, n):                               #@mark
                    if g[r][c] == 0:                                #@mark
                        g[r][0] = 0                                 #@mark
                        g[0][c] = 0                                 #@mark
            for r in range(1, m):                                   #@fill
                for c in range(1, n):                               #@fill
                    if g[r][0] == 0 or g[0][c] == 0:                #@fill
                        g[r][c] = 0                                 #@fill
            if row0:                                                #@row0
                for c in range(n):                                  #@row0
                    g[0][c] = 0                                     #@row0
            if col0:                                                #@col0
                for r in range(m):                                  #@col0
                    g[r][0] = 0                                     #@col0
            return g                                                #@ret
    """,
    "java": """
        static int[][] setZeroes(int[][] g) {
            int m = g.length, n = g[0].length;                      //@size
            boolean row0 = false, col0 = false;                     //@flags
            for (int c = 0; c < n; c++) if (g[0][c] == 0) row0 = true;  //@flags
            for (int r = 0; r < m; r++) if (g[r][0] == 0) col0 = true;  //@flags
            for (int r = 1; r < m; r++)                             //@mark
                for (int c = 1; c < n; c++)                         //@mark
                    if (g[r][c] == 0) {                             //@mark
                        g[r][0] = 0;                                //@mark
                        g[0][c] = 0;                                //@mark
                    }
            for (int r = 1; r < m; r++)                             //@fill
                for (int c = 1; c < n; c++)                         //@fill
                    if (g[r][0] == 0 || g[0][c] == 0) g[r][c] = 0;  //@fill
            if (row0) for (int c = 0; c < n; c++) g[0][c] = 0;      //@row0
            if (col0) for (int r = 0; r < m; r++) g[r][0] = 0;      //@col0
            return g;                                               //@ret
        }
    """,
    "cpp": """
        vector<vector<int>>& setZeroes(vector<vector<int>>& g) {
            int m = g.size(), n = g[0].size();                      //@size
            bool row0 = false, col0 = false;                        //@flags
            for (int c = 0; c < n; c++) if (g[0][c] == 0) row0 = true;  //@flags
            for (int r = 0; r < m; r++) if (g[r][0] == 0) col0 = true;  //@flags
            for (int r = 1; r < m; r++)                             //@mark
                for (int c = 1; c < n; c++)                         //@mark
                    if (g[r][c] == 0) {                             //@mark
                        g[r][0] = 0;                                //@mark
                        g[0][c] = 0;                                //@mark
                    }
            for (int r = 1; r < m; r++)                             //@fill
                for (int c = 1; c < n; c++)                         //@fill
                    if (g[r][0] == 0 || g[0][c] == 0) g[r][c] = 0;  //@fill
            if (row0) for (int c = 0; c < n; c++) g[0][c] = 0;      //@row0
            if (col0) for (int r = 0; r < m; r++) g[r][0] = 0;      //@col0
            return g;                                               //@ret
        }
    """,
    "c": """
        void setZeroes(int m, int n, int g[m][n]) {
            bool row0 = false, col0 = false;                        //@flags
            for (int c = 0; c < n; c++) if (g[0][c] == 0) row0 = true;  //@flags
            for (int r = 0; r < m; r++) if (g[r][0] == 0) col0 = true;  //@flags
            for (int r = 1; r < m; r++)                             //@mark
                for (int c = 1; c < n; c++)                         //@mark
                    if (g[r][c] == 0) {                             //@mark
                        g[r][0] = 0;                                //@mark
                        g[0][c] = 0;                                //@mark
                    }
            for (int r = 1; r < m; r++)                             //@fill
                for (int c = 1; c < n; c++)                         //@fill
                    if (g[r][0] == 0 || g[0][c] == 0) g[r][c] = 0;  //@fill
            if (row0) for (int c = 0; c < n; c++) g[0][c] = 0;      //@row0
            if (col0) for (int r = 0; r < m; r++) g[r][0] = 0;      //@col0
        }
    """,
}
ZERO_RUN = {
    "python": """
        for g in ([[1, 2, 3, 4], [5, 0, 7, 8], [9, 10, 11, 0], [13, 14, 15, 16]], [[0, 1, 2], [3, 4, 5], [6, 7, 8]]):
            for row in set_zeroes(g):
                print(*row)
            print("-")
    """,
    "java": """
        static void show(int[][] g) {
            for (int[] row : g) {
                StringBuilder sb = new StringBuilder();
                for (int x : row) sb.append(sb.length() > 0 ? " " : "").append(x);
                System.out.println(sb);
            }
            System.out.println("-");
        }

        public static void main(String[] args) {
            show(setZeroes(new int[][] {{1, 2, 3, 4}, {5, 0, 7, 8}, {9, 10, 11, 0}, {13, 14, 15, 16}}));
            show(setZeroes(new int[][] {{0, 1, 2}, {3, 4, 5}, {6, 7, 8}}));
        }
    """,
    "cpp": """
        void show(const vector<vector<int>>& g) {
            for (auto& row : g) {
                for (size_t i = 0; i < row.size(); i++) cout << (i ? " " : "") << row[i];
                cout << "\\n";
            }
            cout << "-\\n";
        }

        int main() {
            vector<vector<int>> a = {{1, 2, 3, 4}, {5, 0, 7, 8}, {9, 10, 11, 0}, {13, 14, 15, 16}};
            vector<vector<int>> b = {{0, 1, 2}, {3, 4, 5}, {6, 7, 8}};
            show(setZeroes(a));
            show(setZeroes(b));
        }
    """,
    "c": """
        static void show(int m, int n, int g[m][n]) {
            for (int r = 0; r < m; r++) {
                for (int c = 0; c < n; c++) printf(c ? " %d" : "%d", g[r][c]);
                printf("\\n");
            }
            printf("-\\n");
        }

        int main(void) {
            int a[4][4] = {{1, 2, 3, 4}, {5, 0, 7, 8}, {9, 10, 11, 0}, {13, 14, 15, 16}};
            int b[3][3] = {{0, 1, 2}, {3, 4, 5}, {6, 7, 8}};
            setZeroes(4, 4, a);
            show(4, 4, a);
            setZeroes(3, 3, b);
            show(3, 3, b);
            return 0;
        }
    """,
}

SPREAD = {
    "python": """
        def spread(g):
            m, n = len(g), len(g[0])                                #@size
            for r in range(m):                                      #@each
                for c in range(n):                                  #@each
                    lit = g[r][c] & 1                               #@old
                    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):   #@nb
                        rr, cc = r + dr, c + dc                     #@nb
                        if 0 <= rr < m and 0 <= cc < n and g[rr][cc] & 1:   #@nb
                            lit = 1                                 #@nb
                    g[r][c] |= lit << 1                             #@new
            for r in range(m):                                      #@shift
                for c in range(n):                                  #@shift
                    g[r][c] >>= 1                                   #@shift
            return g                                                #@ret
    """,
    "java": """
        static final int[] DR = {1, -1, 0, 0}, DC = {0, 0, 1, -1};

        static int[][] spread(int[][] g) {
            int m = g.length, n = g[0].length;                      //@size
            for (int r = 0; r < m; r++)                             //@each
                for (int c = 0; c < n; c++) {                       //@each
                    int lit = g[r][c] & 1;                          //@old
                    for (int d = 0; d < 4; d++) {                   //@nb
                        int rr = r + DR[d], cc = c + DC[d];         //@nb
                        if (rr >= 0 && rr < m && cc >= 0 && cc < n && (g[rr][cc] & 1) == 1) lit = 1;  //@nb
                    }
                    g[r][c] |= lit << 1;                            //@new
                }
            for (int r = 0; r < m; r++)                             //@shift
                for (int c = 0; c < n; c++) g[r][c] >>= 1;          //@shift
            return g;                                               //@ret
        }
    """,
    "cpp": """
        vector<vector<int>>& spread(vector<vector<int>>& g) {
            const int DR[] = {1, -1, 0, 0}, DC[] = {0, 0, 1, -1};
            int m = g.size(), n = g[0].size();                      //@size
            for (int r = 0; r < m; r++)                             //@each
                for (int c = 0; c < n; c++) {                       //@each
                    int lit = g[r][c] & 1;                          //@old
                    for (int d = 0; d < 4; d++) {                   //@nb
                        int rr = r + DR[d], cc = c + DC[d];         //@nb
                        if (rr >= 0 && rr < m && cc >= 0 && cc < n && (g[rr][cc] & 1)) lit = 1;  //@nb
                    }
                    g[r][c] |= lit << 1;                            //@new
                }
            for (auto& row : g)                                     //@shift
                for (int& x : row) x >>= 1;                         //@shift
            return g;                                               //@ret
        }
    """,
    "c": """
        void spread(int m, int n, int g[m][n]) {
            const int DR[] = {1, -1, 0, 0}, DC[] = {0, 0, 1, -1};
            for (int r = 0; r < m; r++)                             //@each
                for (int c = 0; c < n; c++) {                       //@each
                    int lit = g[r][c] & 1;                          //@old
                    for (int d = 0; d < 4; d++) {                   //@nb
                        int rr = r + DR[d], cc = c + DC[d];         //@nb
                        if (rr >= 0 && rr < m && cc >= 0 && cc < n && (g[rr][cc] & 1)) lit = 1;  //@nb
                    }
                    g[r][c] |= lit << 1;                            //@new
                }
            for (int r = 0; r < m; r++)                             //@shift
                for (int c = 0; c < n; c++) g[r][c] >>= 1;          //@shift
        }
    """,
}
SPREAD_RUN = {
    "python": """
        for row in spread([[0, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0]]):
            print(*row)
    """,
    "java": """
        public static void main(String[] args) {
            for (int[] row : spread(new int[][] {{0, 0, 0, 0, 0}, {0, 1, 0, 0, 0}, {0, 0, 0, 0, 1}, {0, 0, 0, 0, 0}})) {
                StringBuilder sb = new StringBuilder();
                for (int x : row) sb.append(sb.length() > 0 ? " " : "").append(x);
                System.out.println(sb);
            }
        }
    """,
    "cpp": """
        int main() {
            vector<vector<int>> g = {{0, 0, 0, 0, 0}, {0, 1, 0, 0, 0}, {0, 0, 0, 0, 1}, {0, 0, 0, 0, 0}};
            for (auto& row : spread(g)) {
                for (size_t i = 0; i < row.size(); i++) cout << (i ? " " : "") << row[i];
                cout << "\\n";
            }
        }
    """,
    "c": """
        int main(void) {
            int g[4][5] = {{0, 0, 0, 0, 0}, {0, 1, 0, 0, 0}, {0, 0, 0, 0, 1}, {0, 0, 0, 0, 0}};
            spread(4, 5, g);
            for (int r = 0; r < 4; r++) {
                for (int c = 0; c < 5; c++) printf(c ? " %d" : "%d", g[r][c]);
                printf("\\n");
            }
            return 0;
        }
    """,
}

# ---------------------------------------------------------------- numbers, computed

set_zeroes = py(ZERO["python"], "set_zeroes")
spread = py(SPREAD["python"], "spread")


def copy(g):
    return [list(r) for r in g]


G = [[1, 2, 3, 4], [5, 0, 7, 8], [9, 10, 11, 0], [13, 14, 15, 16]]
GM, GN = 4, 4
ZEROS = [(r, c) for r in range(GM) for c in range(GN) if G[r][c] == 0]
GOUT = set_zeroes(copy(G))
expect = [[0 if any(G[r][k] == 0 for k in range(GN)) or any(G[k][c] == 0 for k in range(GM)) else G[r][c] for c in range(GN)] for r in range(GM)]
assert GOUT == expect

# What goes wrong if you zero rows and columns as you find zeros.
naive = copy(G)
for r in range(GM):
    for c in range(GN):
        if naive[r][c] == 0:
            for k in range(GN):
                naive[r][k] = 0
            for k in range(GM):
                naive[k][c] = 0
NAIVE_LEFT = sum(1 for r in naive for x in r if x)
assert NAIVE_LEFT < sum(1 for r in GOUT for x in r if x)

# Walkthrough of the marker version.
zw = Steps(f"`set_zeroes` on a {GM} × {GN} grid: every row and column holding a 0 becomes all 0s.")
g = copy(G)
zw.step(f"The zeros are at {' and '.join(f'({r}, {c})' for r, c in ZEROS)}. So rows {', '.join(str(r) for r, _ in ZEROS)} and columns {', '.join(str(c) for _, c in ZEROS)} must be wiped.",
        Grid(g, st={z: "answer" for z in ZEROS}))
row0 = any(g[0][c] == 0 for c in range(GN))
col0 = any(g[r][0] == 0 for r in range(GM))
zw.step(f"Before using the first row and column as notepads, save what they say about themselves: does row 0 hold a 0? {'Yes' if row0 else 'No'}. Does column 0? {'Yes' if col0 else 'No'}.",
        Grid(g, st={**{(0, c): "dim" for c in range(GN)}, **{(r, 0): "dim" for r in range(GM)}}), M({"row 0 had a 0": row0, "column 0 had a 0": col0}))
for r in range(1, GM):
    for c in range(1, GN):
        if g[r][c] == 0:
            g[r][0] = 0
            g[0][c] = 0
            zw.step(f"Scanning the inside: ({r}, {c}) is 0. Write a 0 at the start of its row, ({r}, 0), and at the top of its column, (0, {c}). Those two cells are now notes.",
                    Grid(copy(g), st={(r, c): "answer", (r, 0): "mark", (0, c): "mark"}), M({"row 0 had a 0": row0, "column 0 had a 0": col0}))
notes = {(r, 0): "mark" for r in range(1, GM) if g[r][0] == 0}
notes.update({(0, c): "mark" for c in range(1, GN) if g[0][c] == 0})
for r in range(1, GM):
    for c in range(1, GN):
        if g[r][0] == 0 or g[0][c] == 0:
            g[r][c] = 0
zw.step("Now fill the inside: a cell becomes 0 if the note at the start of its row or the top of its column says 0.",
        Grid(copy(g), st={**notes, **{(r, c): "new" for r in range(1, GM) for c in range(1, GN) if g[r][c] == 0 and G[r][c] != 0}}))
assert not row0 and not col0  # the text of the next step says so
if row0:
    for c in range(GN):
        g[0][c] = 0
if col0:
    for r in range(GM):
        g[r][0] = 0
zw.step(f"Last, the first row and column themselves, using the two saved answers. Neither held a 0 to begin with, so the notes we wrote there are already the right result for them.",
        Grid(copy(g), st={(r, c): "found" for r in range(GM) for c in range(GN) if g[r][c] != 0}), result="done")
assert g == GOUT

# A zero in the first row: why the two flags are needed.
F = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
FOUT = set_zeroes(copy(F))
assert FOUT == [[0, 0, 0], [0, 4, 5], [0, 7, 8]]

# Spread with two bits per cell.
S = [[0, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0]]
SM, SN = 4, 5
SOUT = spread(copy(S))


def bits(g):
    return [[f"{x:02b}" for x in row] for row in g]


sw = Steps("`spread`: a cell is lit next if it, or a neighbour above, below, left or right, is lit now. Every cell changes at once.")
g = copy(S)
sw.step("Each cell is written as two bits. The right bit is *now*. The left bit will hold *next*, and starts as 0.", Grid(bits(g)))
for r in range(SM):
    for c in range(SN):
        lit = g[r][c] & 1
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            rr, cc = r + dr, c + dc
            if 0 <= rr < SM and 0 <= cc < SN and g[rr][cc] & 1:
                lit = 1
        g[r][c] |= lit << 1
    newly = [(r, c) for c in range(SN) if g[r][c] & 2]
    sw.step(f"Row {r}: for each cell, look only at the right bits (`& 1`), which still say *now* even for cells already updated. "
            + (f"Cells {', '.join(f'({a}, {b})' for a, b in newly)} get a 1 in the left bit." if newly else "No cell in this row will be lit."),
            Grid(bits(g), st={**{(r, c): "active" for c in range(SN)}, **{rc: "new" for rc in newly}}))
for r in range(SM):
    for c in range(SN):
        g[r][c] >>= 1
sw.step("Every cell has its next state in the left bit. Shift right by one: the left bit becomes the value, and the old one falls away.",
        Grid(g, st={(r, c): "found" for r in range(SM) for c in range(SN) if g[r][c]}))
assert g == SOUT
WRONG = copy(S)
for r in range(SM):
    for c in range(SN):
        if any(0 <= r + dr < SM and 0 <= c + dc < SN and WRONG[r + dr][c + dc] for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            WRONG[r][c] = 1
WRONG_LIT = sum(map(sum, WRONG))
assert WRONG_LIT > sum(map(sum, SOUT))

CODES = [("0", "00", "off now, off next"), ("1", "01", "on now, off next"), ("2", "10", "off now, on next"), ("3", "11", "on now, on next")]

# Spare range: two values 0..255 in one cell.
OLD, NEW = 200, 137
PACKED = OLD + 256 * NEW
assert PACKED % 256 == OLD and PACKED // 256 == NEW

lesson(
    "arrays-hashing",
    "matrix-in-place",
    """
    Updating a grid in place is hard when each new value depends on old values you may already have overwritten. The
    fix is to hide the extra information inside the grid itself: in its first row and column, or in spare bits of each
    cell. Then the update needs no second grid, only O(1) extra space.
    """,
    [
        ("idea", "The idea", [
            """
            Think of a teacher marking a big wall chart of student results. Every time they find a problem in a row,
            the whole row should be crossed out, and the same for every column. If they cross things out as they go,
            the crossings themselves look like new problems, and soon the whole chart is crossed out.

            The fix is to make notes first and cross out later. The teacher could keep a separate list of bad rows and
            bad columns, but there's no paper. So they write the notes on the chart itself, in the margin: the first
            cell of each row and the top cell of each column. Once every note is written, they go back and cross out
            using the notes.

            That's the whole pattern. The grid has spare room somewhere (its first row and column, unused bits, values
            that can't occur) and you use it to hold "what I still need to know" while you work.
            """,
            fig(Grid(G, st={z: "answer" for z in ZEROS}, label="the zeros"),
                Grid(naive, st={(r, c): "dim" for r in range(GM) for c in range(GN) if naive[r][c] == 0}, label="wiping as you go"),
                Grid(GOUT, st={(r, c): "dim" for r in range(GM) for c in range(GN) if GOUT[r][c] == 0}, label="the right answer"),
                caption=f"Wiping rows and columns the moment you see a 0 creates new zeros, which wipe more. Only {NAIVE_LEFT} cells survive instead of {sum(1 for r in GOUT for x in r if x)}."),
            key("""
            Never let a new value be read as an old one. Either note what to change in spare room (the first row and
            column, saved with two flags) and change it afterwards, or keep both versions in one cell: the old in the
            low bits, the new in the high bits, then shift.
            """),
        ]),
        ("signals", "When to reach for it", [
            """
            A grid update where "every cell changes at the same moment, based on the board as it was", and the question
            says "in place", "without a second grid" or "O(1) extra space". Typical cases: wipe rows and columns that
            contain something, apply a neighbour rule to every cell at once (cellular automata, blurring, spreading),
            mark cells for a second pass.

            Ask two questions. Is there information I'd normally keep in a separate array (one flag per row, one per
            column)? Then maybe the first row and column can hold it. Does each cell have room for more than its own
            value (0/1 cells in an `int`, small values with lots of headroom)? Then the cell can hold old and new
            together.

            Not a fit:

            - Extra memory is allowed. A copy of the grid is simpler and just as fast; use it.
            - Cells already use their full range (any `int` at all). There are no spare bits to borrow.
            - The update is naturally in order (each cell depends only on cells you haven't touched yet). Then a plain
              loop in the right direction is enough.
            """,
        ]),
        ("theory", "Why it works", [
            """
            ### The problem: reading what you just wrote

            In a "simultaneous" update, every new value is computed from old values. Loop through the grid writing new
            values, and by the time you reach a cell, some of its neighbours already hold new ones. Use them by mistake
            and the change leaks across the grid, as in the picture above. Every in-place trick is a way to keep the old
            values readable until nobody needs them any more.

            ### Notes in the first row and column

            Wiping rows and columns needs `m + n` facts: "does row `r` contain a 0?" and "does column `c`?". The first
            column has a cell for every row, and the first row has a cell for every column, so they can hold those facts.
            The catch is that they hold real data too, including facts about themselves. So:

            1. Save two booleans first: does the first row contain a 0? Does the first column?
            2. Scan the rest of the grid. For each 0 at `(r, c)`, write 0 into `(r, 0)` and `(0, c)`.
            3. Fill the rest of the grid from the notes.
            4. Only now wipe the first row and column, if the two booleans say so.

            The order matters. Wiping the first row in step 2 would put a 0 at the top of every column, and every
            column would look like it needs wiping. Writing a note can't do damage, because a cell only gets a note when
            its row (or column) is going to be wiped anyway.
            """,
            table(["step", "reads", "writes"],
                  ["save two flags", "first row, first column", "two booleans"],
                  ["write notes", "the rest of the grid", "first row, first column"],
                  ["fill from notes", "first row, first column", "the rest of the grid"],
                  ["finish the edges", "two booleans", "first row, first column"]),
            """
            ### Two states in one cell

            For cells that are 0 or 1, an `int` has plenty of spare bits. Keep *now* in bit 0 and write *next* into
            bit 1. Reading `cell & 1` always gives *now*, whether or not that cell has been updated yet. When every cell
            has its *next*, shift everything right by one: `cell >>= 1`.
            """,
            table(["cell", "bits", "meaning"], *CODES),
            f"""
            You can use any encoding that keeps the old value readable, such as the numbers 2 and 3 meaning "was on, will
            be off" and "was off, will be on". Bits are just the tidiest: the old value is always `& 1`.

            ### Two numbers in one cell

            The same idea works for bigger values if they have a known limit. If every value is below 256, store the new
            value as `cell + 256 · new`. The old value is `cell % 256` and the new one is `cell // 256`. For example, old
            {OLD} and new {NEW} pack into {PACKED}: `{PACKED} % 256 = {OLD}` and `{PACKED} // 256 = {NEW}`. The base just has to
            be bigger than any old value, and the packed number has to fit in the type.
            """,
        ]),
        ("template", "The template", [
            "Wipe every row and every column that contains a 0, using only O(1) extra space.",
            code(
                "Set rows and columns to zero with first-row and first-column notes",
                ZERO,
                [
                    ("size", "Rows and columns."),
                    ("flags", "Before the first row and column become notepads, save whether they contain a 0 themselves.",
                     {"c": "C gets the sizes from the caller, and the grid as a variable-length 2D array so `g[r][c]` works."}),
                    ("mark", "Scan everything except the first row and column. Each 0 leaves a note at the start of its row "
                             "and the top of its column."),
                    ("fill", "Wipe each inner cell whose row or column has a note. The notes themselves aren't touched."),
                    ("row0", "The first row is wiped only if it held a 0 to begin with."),
                    ("col0", "Same for the first column. These two come last, so no note is destroyed before it's read."),
                    ("ret", "The same grid, changed in place.",
                     {"python": "Returning the grid is a convenience; the caller's list of lists has already changed."}),
                ],
                ZERO_RUN,
                "set_zeroes on a 4 × 4 grid with zeros at (1, 1) and (2, 3); then on a grid with a 0 in its corner",
            ),
            f"""
            The second grid has its only 0 in the corner, so both flags are true: the first row and first column are
            wiped and nothing else is. Without the flags, the corner 0 would look like a note for both the first row and
            the first column, and there'd be no way to tell a note from a real 0.
            """,
        ]),
        ("trace", "Trace it by hand", [
            "Notes first, wiping second, edges last:",
            walk(zw),
        ]),
        ("examples", "More examples", [
            """
            ### Spreading one step

            Lit cells light up their neighbours: after one step, a cell is lit if it or any cell directly above, below,
            left or right of it was lit. Every cell changes at once. If you light cells as you go, a light you just
            switched on lights the next cell, and so on, and the light races across the grid in one step. With two bits
            per cell, it can't:
            """,
            walk(sw),
            fig(Grid(S, st={(r, c): "found" for r in range(SM) for c in range(SN) if S[r][c]}, label="before"),
                Grid(SOUT, st={(r, c): "found" for r in range(SM) for c in range(SN) if SOUT[r][c]}, label="after one step (right)"),
                Grid(WRONG, st={(r, c): "dim" for r in range(SM) for c in range(SN) if WRONG[r][c]}, label="lighting as you go (wrong)"),
                caption=f"Done in place without the extra bit, {WRONG_LIT} cells end up lit instead of {sum(map(sum, SOUT))}: new lights were read as old ones."),
            """
            ### Rules with counts

            Many rules count neighbours ("lit if exactly two neighbours are lit"). The count is computed from the old
            values (`& 1`) and the decision goes in bit 1, exactly as above. The rule changes; the bookkeeping doesn't.

            ### Marking cells for later

            Sometimes the first pass only *finds* cells (say, every cell to be removed) and a second pass acts on them.
            If the values have a range that can't occur, such as negatives in a grid of counts, a negative copy of the
            value is a mark that keeps the original recoverable, just like *In-place index marking*.
            """,
        ]),
        ("variations", "Variations", [
            """
            ### Old in bit 0, new in bit 1

            The spreading rule as code. The structure is the same for any rule on a 0/1 grid: compute from `& 1`,
            store with `|= next << 1`, then shift.
            """,
            code(
                "Spread lit cells one step, in place",
                SPREAD,
                [
                    ("size", "Rows and columns."),
                    ("each", "Visit every cell once."),
                    ("old", "This cell's *current* state. Bit 0 hasn't changed, even if bit 1 has been written."),
                    ("nb", "Look at the four neighbours that are inside the grid, reading only their bit 0.",
                     {"java": "`(g[rr][cc] & 1) == 1`: Java won't treat an `int` as a condition.",
                      "cpp": "The direction arrays are declared once at the top; `& 1` is already a usable condition in C++."}),
                    ("new", "Store the next state in bit 1. `|=` leaves bit 0 alone."),
                    ("shift", "Every next state is ready. Shift right: bit 1 becomes the value and bit 0 is dropped."),
                    ("ret", "The grid one step later."),
                ],
                SPREAD_RUN,
                "spread on a 4 × 5 grid with lit cells at (1, 1) and (2, 4)",
            ),
            """
            ### Rotating or transposing a square grid

            Not every in-place grid job needs notes. Rotating a square grid by 90° moves values along cycles of four
            positions, so a single temporary per cycle is enough (or a transpose followed by mirroring each row). See
            *Matrix traversal* for the index maps. Markers are for the jobs where the new value of a cell depends on
            *other* cells' old values.

            ### Choosing where to keep the notes

            Use whatever spare room the problem gives you: the first row and column when cells are arbitrary, spare bits
            when cells are small, impossible values (negatives, a value above the maximum) when the range is known. If
            none of those exist, O(1) space probably isn't possible, and a copy is the honest answer.
            """,
        ]),
        ("complexity", "What it costs", [
            """
            Each method reads and writes every cell a constant number of times: O(m·n) time. The extra memory is two
            booleans, or nothing at all, so O(1). Compare that with a second grid (O(m·n) extra) or separate row and
            column flag arrays (O(m + n) extra).

            With the neighbour rule, each cell looks at a fixed number of neighbours (4 here, 8 with diagonals), so it's
            still O(m·n).
            """,
            table(
                ["Approach", "Time", "Extra space"],
                ["Copy the grid, update from the copy", "O(m·n)", "O(m·n)"],
                ["Row and column flag arrays", "O(m·n)", "O(m + n)"],
                ["Notes in the first row and column", "O(m·n)", "O(1)"],
                ["Old and new in one cell (bits or a base)", "O(m·n)", "O(1)"],
            ),
        ]),
        ("languages", "In your language", [
            """
            ### Python

            `g[r][c] & 1`, `|=` and `>>=` work on ints as you'd expect. A grid made with `[[0] * n] * m` shares the same row
            `m` times, so one write changes every row; build it with `[[0] * n for _ in range(m)]`. `any(...)` makes the
            two flags one line each.

            ### Java

            `int[][]` is an array of row arrays, so `g[r][c]` updates the caller's grid. Bit tests need a comparison:
            `(x & 1) == 1`. Be careful with operator precedence: `x & 1 == 1` parses as `x & (1 == 1)` and doesn't compile.

            ### C++

            Take the grid by reference (`vector<vector<int>>&`), or your changes vanish with the copy. `x & 1` is a fine
            condition. Mind precedence here too: `x & 1 == 1` means `x & (1 == 1)`, which compiles and is wrong.

            ### C

            Pass the sizes and the grid as `int g[m][n]` (a variable-length array parameter), or as a flat `int*` with
            `g[r * n + c]`. Shifting negative numbers right is implementation-defined, so keep the bit tricks for values
            that are never negative.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            - Wiping the first row or column before the notes are read. Edges always go last.
            - Forgetting the two flags, so a real 0 in the first row is confused with a note.
            - Starting the note scan at row 0 or column 0. The notepad cells are handled by the flags.
            - Reading a neighbour's full value instead of `& 1` after some cells have bit 1 set.
            - Forgetting the final shift, so cells hold 2s and 3s.
            - Packing values with a base that's too small, or a packed number that overflows the type.
            - A 1 × n or m × 1 grid: the "inside" is empty and only the flags do any work. Check that this still works.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("Why does wiping rows and columns as soon as you see a 0 give the wrong answer?",
                 "The wiped cells become new zeros, and when the scan reaches them they wipe their own rows and columns. Zeros that weren't in the original grid spread."),
                ("Why must the first row and column be wiped last?",
                 "They hold the notes. Wiping the first row early would put a 0 at the top of every column, and every column would then look like it needs wiping."),
                ("What are the two flags for?",
                 "The first row and column are used for notes, so a 0 written there can't tell you whether that row or column held a 0 originally. The flags save that before any notes are written."),
                ("In the two-bit method, why is it safe to read a neighbour that has already been updated?",
                 "Only bit 1 was written. Bit 0 still holds its current state, and the rule only reads `& 1`."),
                ("Values are 0 to 999 and new values are too. How could one int hold both?",
                 "Store cell + 1000 · new. The old value is cell % 1000 and the new one is cell // 1000 (as long as 1000 · 999 + 999 fits in the type)."),
            ),
        ]),
    ],
)
