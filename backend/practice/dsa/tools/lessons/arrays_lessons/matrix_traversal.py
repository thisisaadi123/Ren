"""Lesson: Matrix traversal (Arrays & Hashing, pattern 7)."""
from lesson import Bars, Grid, M, Row, Steps, code, fig, key, lesson, py, quiz, table, walk

# ---------------------------------------------------------------- the code

ZIGZAG = {
    "python": """
        def zigzag(grid):
            m, n = len(grid), len(grid[0])                          #@size
            out = []                                                #@size
            for d in range(m + n - 1):                              #@diag
                cells = []                                          #@cells
                for r in range(max(0, d - n + 1), min(m, d + 1)):   #@rows
                    cells.append(grid[r][d - r])                    #@cells
                if d % 2 == 0:                                      #@flip
                    cells.reverse()                                 #@flip
                out.extend(cells)                                   #@out
            return out                                              #@ret
    """,
    "java": """
        static List<Integer> zigzag(int[][] grid) {
            int m = grid.length, n = grid[0].length;                //@size
            List<Integer> out = new ArrayList<>();                  //@size
            for (int d = 0; d < m + n - 1; d++) {                   //@diag
                List<Integer> cells = new ArrayList<>();            //@cells
                for (int r = Math.max(0, d - n + 1); r < Math.min(m, d + 1); r++) {  //@rows
                    cells.add(grid[r][d - r]);                      //@cells
                }
                if (d % 2 == 0) Collections.reverse(cells);         //@flip
                out.addAll(cells);                                  //@out
            }
            return out;                                             //@ret
        }
    """,
    "cpp": """
        vector<int> zigzag(const vector<vector<int>>& grid) {
            int m = grid.size(), n = grid[0].size();                //@size
            vector<int> out;                                        //@size
            for (int d = 0; d < m + n - 1; d++) {                   //@diag
                vector<int> cells;                                  //@cells
                for (int r = max(0, d - n + 1); r < min(m, d + 1); r++) {  //@rows
                    cells.push_back(grid[r][d - r]);                //@cells
                }
                if (d % 2 == 0) reverse(cells.begin(), cells.end());  //@flip
                out.insert(out.end(), cells.begin(), cells.end());  //@out
            }
            return out;                                             //@ret
        }
    """,
    "c": """
        // grid is m x n, stored row by row (cell (r, c) at r * n + c). Writes m * n values to out.
        void zigzag(const int* grid, int m, int n, int* out) {
            int k = 0;                                              //@size
            for (int d = 0; d < m + n - 1; d++) {                   //@diag
                int lo = d - n + 1 > 0 ? d - n + 1 : 0;             //@rows
                int hi = d < m - 1 ? d : m - 1;                     //@rows
                for (int i = 0; i <= hi - lo; i++) {                //@cells
                    int r = d % 2 == 0 ? hi - i : lo + i;           //@flip
                    out[k++] = grid[r * n + (d - r)];               //@out
                }
            }
        }
    """,
}
ZIGZAG_RUN = {
    "python": """
        print(*zigzag([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]))
        print(*zigzag([[7], [8], [9]]))
    """,
    "java": """
        public static void main(String[] args) {
            for (int[][] g : new int[][][] {{{1, 2, 3, 4}, {5, 6, 7, 8}, {9, 10, 11, 12}}, {{7}, {8}, {9}}}) {
                StringBuilder sb = new StringBuilder();
                for (int x : zigzag(g)) sb.append(sb.length() > 0 ? " " : "").append(x);
                System.out.println(sb);
            }
        }
    """,
    "cpp": """
        int main() {
            for (auto& g : vector<vector<vector<int>>>{{{1, 2, 3, 4}, {5, 6, 7, 8}, {9, 10, 11, 12}}, {{7}, {8}, {9}}}) {
                auto v = zigzag(g);
                for (size_t i = 0; i < v.size(); i++) cout << (i ? " " : "") << v[i];
                cout << "\\n";
            }
        }
    """,
    "c": """
        int main(void) {
            int a[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}, b[] = {7, 8, 9}, out[12];
            zigzag(a, 3, 4, out);
            for (int i = 0; i < 12; i++) printf(i ? " %d" : "%d", out[i]);
            printf("\\n");
            zigzag(b, 3, 1, out);
            for (int i = 0; i < 3; i++) printf(i ? " %d" : "%d", out[i]);
            printf("\\n");
            return 0;
        }
    """,
}

PEAKS = {
    "python": """
        DR = [-1, 1, 0, 0]                                          #@dirs
        DC = [0, 0, -1, 1]                                          #@dirs

        def count_peaks(grid):
            m, n = len(grid), len(grid[0])                          #@size
            peaks = 0                                               #@size
            for r in range(m):                                      #@cells
                for c in range(n):                                  #@cells
                    ok = True                                       #@each
                    for k in range(4):                              #@each
                        nr, nc = r + DR[k], c + DC[k]               #@step
                        if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] >= grid[r][c]:  #@inside
                            ok = False                              #@inside
                    if ok:                                          #@count
                        peaks += 1                                  #@count
            return peaks                                            #@ret
    """,
    "java": """
        static final int[] DR = {-1, 1, 0, 0};                      //@dirs
        static final int[] DC = {0, 0, -1, 1};                      //@dirs

        static int countPeaks(int[][] grid) {
            int m = grid.length, n = grid[0].length, peaks = 0;     //@size
            for (int r = 0; r < m; r++) {                           //@cells
                for (int c = 0; c < n; c++) {                       //@cells
                    boolean ok = true;                              //@each
                    for (int k = 0; k < 4; k++) {                   //@each
                        int nr = r + DR[k], nc = c + DC[k];         //@step
                        if (nr >= 0 && nr < m && nc >= 0 && nc < n && grid[nr][nc] >= grid[r][c]) ok = false;  //@inside
                    }
                    if (ok) peaks++;                                //@count
                }
            }
            return peaks;                                           //@ret
        }
    """,
    "cpp": """
        const int DR[4] = {-1, 1, 0, 0};                            //@dirs
        const int DC[4] = {0, 0, -1, 1};                            //@dirs

        int countPeaks(const vector<vector<int>>& grid) {
            int m = grid.size(), n = grid[0].size(), peaks = 0;     //@size
            for (int r = 0; r < m; r++) {                           //@cells
                for (int c = 0; c < n; c++) {                       //@cells
                    bool ok = true;                                 //@each
                    for (int k = 0; k < 4; k++) {                   //@each
                        int nr = r + DR[k], nc = c + DC[k];         //@step
                        if (nr >= 0 && nr < m && nc >= 0 && nc < n && grid[nr][nc] >= grid[r][c]) ok = false;  //@inside
                    }
                    if (ok) peaks++;                                //@count
                }
            }
            return peaks;                                           //@ret
        }
    """,
    "c": """
        static const int DR[4] = {-1, 1, 0, 0};                     //@dirs
        static const int DC[4] = {0, 0, -1, 1};                     //@dirs

        int countPeaks(const int* grid, int m, int n) {
            int peaks = 0;                                          //@size
            for (int r = 0; r < m; r++) {                           //@cells
                for (int c = 0; c < n; c++) {                       //@cells
                    bool ok = true;                                 //@each
                    for (int k = 0; k < 4; k++) {                   //@each
                        int nr = r + DR[k], nc = c + DC[k];         //@step
                        if (nr >= 0 && nr < m && nc >= 0 && nc < n && grid[nr * n + nc] >= grid[r * n + c]) ok = false;  //@inside
                    }
                    if (ok) peaks++;                                //@count
                }
            }
            return peaks;                                           //@ret
        }
    """,
}
PEAKS_RUN = {
    "python": """
        print(count_peaks([[1, 4, 2, 2], [3, 1, 5, 1], [2, 6, 1, 3]]))
        print(count_peaks([[5, 5], [5, 5]]))
    """,
    "java": """
        public static void main(String[] args) {
            System.out.println(countPeaks(new int[][] {{1, 4, 2, 2}, {3, 1, 5, 1}, {2, 6, 1, 3}}));
            System.out.println(countPeaks(new int[][] {{5, 5}, {5, 5}}));
        }
    """,
    "cpp": """
        int main() {
            cout << countPeaks({{1, 4, 2, 2}, {3, 1, 5, 1}, {2, 6, 1, 3}}) << "\\n" << countPeaks({{5, 5}, {5, 5}}) << "\\n";
        }
    """,
    "c": """
        int main(void) {
            int a[] = {1, 4, 2, 2, 3, 1, 5, 1, 2, 6, 1, 3}, b[] = {5, 5, 5, 5};
            printf("%d\\n%d\\n", countPeaks(a, 3, 4), countPeaks(b, 2, 2));
            return 0;
        }
    """,
}

RINGS = {
    "python": """
        def ring_sums(grid):
            m, n = len(grid), len(grid[0])                          #@size
            sums = [0] * ((min(m, n) + 1) // 2)                     #@count
            for r in range(m):                                      #@cells
                for c in range(n):                                  #@cells
                    k = min(r, c, m - 1 - r, n - 1 - c)             #@ring
                    sums[k] += grid[r][c]                           #@add
            return sums                                             #@ret
    """,
    "java": """
        static long[] ringSums(int[][] grid) {
            int m = grid.length, n = grid[0].length;                //@size
            long[] sums = new long[(Math.min(m, n) + 1) / 2];       //@count
            for (int r = 0; r < m; r++) {                           //@cells
                for (int c = 0; c < n; c++) {                       //@cells
                    int k = Math.min(Math.min(r, c), Math.min(m - 1 - r, n - 1 - c));  //@ring
                    sums[k] += grid[r][c];                          //@add
                }
            }
            return sums;                                            //@ret
        }
    """,
    "cpp": """
        vector<long long> ringSums(const vector<vector<int>>& grid) {
            int m = grid.size(), n = grid[0].size();                //@size
            vector<long long> sums((min(m, n) + 1) / 2, 0);         //@count
            for (int r = 0; r < m; r++) {                           //@cells
                for (int c = 0; c < n; c++) {                       //@cells
                    int k = min({r, c, m - 1 - r, n - 1 - c});      //@ring
                    sums[k] += grid[r][c];                          //@add
                }
            }
            return sums;                                            //@ret
        }
    """,
    "c": """
        static int min2(int a, int b) { return a < b ? a : b; }

        // Writes one sum per ring to sums and returns how many rings there are.
        int ringSums(const int* grid, int m, int n, long long* sums) {
            int rings = (min2(m, n) + 1) / 2;                       //@count
            for (int k = 0; k < rings; k++) sums[k] = 0;            //@count
            for (int r = 0; r < m; r++) {                           //@cells
                for (int c = 0; c < n; c++) {                       //@cells
                    int k = min2(min2(r, c), min2(m - 1 - r, n - 1 - c));  //@ring
                    sums[k] += grid[r * n + c];                     //@add
                }
            }
            return rings;                                           //@ret
        }
    """,
}
RINGS_RUN = {
    "python": """
        print(*ring_sums([[1, 1, 1, 1, 1], [1, 2, 2, 2, 1], [1, 2, 9, 2, 1], [1, 2, 2, 2, 1], [1, 1, 1, 1, 1]]))
        print(*ring_sums([[4, 0, 1], [2, 5, 3]]))
    """,
    "java": """
        public static void main(String[] args) {
            int[][][] cases = {{{1, 1, 1, 1, 1}, {1, 2, 2, 2, 1}, {1, 2, 9, 2, 1}, {1, 2, 2, 2, 1}, {1, 1, 1, 1, 1}}, {{4, 0, 1}, {2, 5, 3}}};
            for (int[][] g : cases) {
                StringBuilder sb = new StringBuilder();
                for (long s : ringSums(g)) sb.append(sb.length() > 0 ? " " : "").append(s);
                System.out.println(sb);
            }
        }
    """,
    "cpp": """
        int main() {
            vector<vector<vector<int>>> cases = {{{1, 1, 1, 1, 1}, {1, 2, 2, 2, 1}, {1, 2, 9, 2, 1}, {1, 2, 2, 2, 1}, {1, 1, 1, 1, 1}}, {{4, 0, 1}, {2, 5, 3}}};
            for (auto& g : cases) {
                auto s = ringSums(g);
                for (size_t i = 0; i < s.size(); i++) cout << (i ? " " : "") << s[i];
                cout << "\\n";
            }
        }
    """,
    "c": """
        int main(void) {
            int a[] = {1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 2, 9, 2, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1}, b[] = {4, 0, 1, 2, 5, 3};
            long long sums[3];
            int k = ringSums(a, 5, 5, sums);
            for (int i = 0; i < k; i++) printf(i ? " %lld" : "%lld", sums[i]);
            printf("\\n");
            k = ringSums(b, 2, 3, sums);
            for (int i = 0; i < k; i++) printf(i ? " %lld" : "%lld", sums[i]);
            printf("\\n");
            return 0;
        }
    """,
}

# ---------------------------------------------------------------- numbers, computed

zigzag = py(ZIGZAG["python"], "zigzag")
count_peaks = py(PEAKS["python"], "count_peaks")
ring_sums = py(RINGS["python"], "ring_sums")

G = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
GM, GN = 3, 4


def order_grid(cells):
    """cells in visit order -> grid of visit numbers (1-based)."""
    out = [[0] * GN for _ in range(GM)]
    for k, (r, c) in enumerate(cells):
        out[r][c] = k + 1
    return out


ROWMAJ = order_grid([(r, c) for r in range(GM) for c in range(GN)])
COLMAJ = order_grid([(r, c) for c in range(GN) for r in range(GM)])
ZZ = []
for d in range(GM + GN - 1):
    cells = [(r, d - r) for r in range(max(0, d - GN + 1), min(GM, d + 1))]
    if d % 2 == 0:
        cells.reverse()
    ZZ += cells
ZIGZAG_ORD = order_grid(ZZ)
assert [G[r][c] for r, c in ZZ] == zigzag(G)
SP, top, bot, lef, rig = [], 0, GM - 1, 0, GN - 1
while top <= bot and lef <= rig:
    SP += [(top, c) for c in range(lef, rig + 1)]
    SP += [(r, rig) for r in range(top + 1, bot + 1)]
    if top < bot:
        SP += [(bot, c) for c in range(rig - 1, lef - 1, -1)]
    if lef < rig:
        SP += [(r, lef) for r in range(bot - 1, top, -1)]
    top, bot, lef, rig = top + 1, bot - 1, lef + 1, rig - 1
SPIRAL_ORD = order_grid(SP)
assert sorted(SP) == sorted((r, c) for r in range(GM) for c in range(GN))

# Flattening: index of (r, c) in row-major order.
FLAT = [[r * GN + c for c in range(GN)] for r in range(GM)]

# Zigzag walkthrough.
zw = Steps(f"Reading `{G}` diagonal by diagonal. Every cell on diagonal d has r + c = d.")
DIAG = [[r + c for c in range(GN)] for r in range(GM)]
zw.step("Label each cell with r + c. Cells with the same number sit on the same diagonal, running from top-right to bottom-left.", Grid(DIAG))
done = []
for d in range(GM + GN - 1):
    cells = [(r, d - r) for r in range(max(0, d - GN + 1), min(GM, d + 1))]
    if d % 2 == 0:
        cells.reverse()
    vals = [G[r][c] for r, c in cells]
    done += vals
    way = "upwards (bottom-left to top-right)" if d % 2 == 0 else "downwards (top-right to bottom-left)"
    rows = f"rows {max(0, d - GN + 1)} to {min(GM, d + 1) - 1}"
    zw.step(f"Diagonal {d}: {rows}, read {way}: {', '.join(map(str, vals))}.",
            Grid(G, st={**{(r, c): "dim" for r in range(GM) for c in range(GN) if r + c < d}, **{rc: "active" for rc in cells}}), M({"read so far": " ".join(map(str, done))}))

# Peaks.
PG = [[1, 4, 2, 2], [3, 1, 5, 1], [2, 6, 1, 3]]
PM_, PN_ = 3, 4
DR, DC = [-1, 1, 0, 0], [0, 0, -1, 1]
peaks = []
for r in range(PM_):
    for c in range(PN_):
        if all(not (0 <= r + DR[k] < PM_ and 0 <= c + DC[k] < PN_) or PG[r + DR[k]][c + DC[k]] < PG[r][c] for k in range(4)):
            peaks.append((r, c))
assert len(peaks) == count_peaks(PG)
pw = Steps(f"Checking a few cells of the grid for peaks: bigger than every neighbour above, below, left and right.")
for (r, c) in [(0, 1), (1, 2), (2, 3), (1, 1)]:
    nb = [(r + DR[k], c + DC[k]) for k in range(4)]
    inside = [(a, b) for a, b in nb if 0 <= a < PM_ and 0 <= b < PN_]
    outside = len(nb) - len(inside)
    is_peak = (r, c) in peaks
    vals = ", ".join(str(PG[a][b]) for a, b in inside)
    msg = (f"({r}, {c}) holds {PG[r][c]}. Its neighbours inside the grid hold {vals}"
           + (f"; {outside} direction{'s' if outside > 1 else ''} fall off the edge and are skipped" if outside else "")
           + (f". All smaller, so it's a peak." if is_peak else f". At least one isn't smaller, so it's not a peak."))
    pw.step(msg, Grid(PG, st={**{rc: "mark" for rc in inside}, (r, c): "answer" if is_peak else "active"}))
pw.step(f"Doing this for every cell finds {len(peaks)} peaks.", Grid(PG, st={rc: "answer" for rc in peaks}), result=len(peaks))

NEIGH = [[" ", "-1,0", " "], ["0,-1", "r,c", "0,+1"], [" ", "+1,0", " "]]

# Rings.
RG5 = [[1, 1, 1, 1, 1], [1, 2, 2, 2, 1], [1, 2, 9, 2, 1], [1, 2, 2, 2, 1], [1, 1, 1, 1, 1]]
RING_IDX = [[min(r, c, 4 - r, 4 - c) for c in range(5)] for r in range(5)]
RING_IDX_46 = [[min(r, c, 3 - r, 5 - c) for c in range(6)] for r in range(4)]
RS = ring_sums(RG5)
assert RS == [16, 16, 9]

# Index maps for common transforms, worked on a 2 x 3 grid.
T = [[1, 2, 3], [4, 5, 6]]
TR = [[T[r][c] for r in range(2)] for c in range(3)]
MIR = [row[::-1] for row in T]
ROT = [[T[2 - 1 - r][c] for r in range(2)] for c in range(3)]
assert ROT == [[4, 1], [5, 2], [6, 3]]

lesson(
    "arrays-hashing",
    "matrix-traversal",
    """
    A grid is just rows of rows, and every grid problem comes down to visiting cells in the right order without
    stepping off the edge. Once you can turn any walk (row by row, by diagonals, around the rings, to the neighbours)
    into simple arithmetic on `r` and `c`, grids stop being scary.
    """,
    [
        ("idea", "The idea", [
            """
            Think of a cinema seating chart. Every seat has a row and a seat number, and an usher can walk the room in
            many ways: row by row, front to back, along a diagonal, or around the outside aisle and inwards. The seats
            don't move. Only the route changes.

            A matrix is the same. `grid[r][c]` is row `r`, column `c`, with `(0, 0)` at the top-left. An `m × n` grid
            has `m` rows and `n` columns. Every traversal problem is about choosing a route and expressing it with
            loops over `r` and `c`. Here are four routes over the same 3 × 4 grid, with each cell showing *when* it gets
            visited:
            """,
            fig(Grid(ROWMAJ, label="row by row"), Grid(COLMAJ, label="column by column"),
                Grid(ZIGZAG_ORD, label="zigzag diagonals"), Grid(SPIRAL_ORD, label="spiral"),
                caption="Same twelve cells, four routes. The numbers are the visit order."),
            key("""
            Pick the route, then describe it with arithmetic: which cells share a diagonal (`r + c`), which share a ring
            (`min(r, c, m-1-r, n-1-c)`), which are neighbours (`r + dr, c + dc`). Then check every step stays inside
            `0 ≤ r < m` and `0 ≤ c < n`.
            """),
        ]),
        ("signals", "When to reach for it", [
            """
            Anything given as a 2D grid, board, image or table: read it in some order, transform it (flip, rotate,
            transpose), look at each cell's neighbours, or work layer by layer from the outside in.

            Words to listen for: "spiral", "diagonal", "zigzag", "rotate the image", "transpose", "neighbours", "adjacent
            cells", "border", "layer", "ring".

            When it's not the whole story:

            - **Connected regions** (islands, flood fill, shortest path through a maze) need BFS or DFS. You still use
              the neighbour arithmetic from this lesson, but the visiting order is driven by a queue or a stack. That's
              the Graphs topic.
            - **Sums over rectangles, asked many times**, want 2D prefix sums (see *Prefix sums*).
            - **Changing the grid in place using markers** (rows and columns that must be zeroed, for example) has its own
              pattern later in this topic, *In-place grid markers*.
            """,
        ]),
        ("theory", "The arithmetic of grids", [
            """
            ### Rows, columns and the flat view

            In memory a grid is usually stored row by row. Cell `(r, c)` of an `m × n` grid is element `r × n + c` of one
            long array, and element `i` is back at `(i // n, i % n)`. That's how the C code in this lesson stores grids,
            and it's also a handy trick in any language: one loop over `i` from 0 to `m × n - 1` visits the whole grid.
            """,
            fig(Grid(FLAT, label="r × 4 + c"), caption="Row-major numbering: the flat index of every cell in a 3 × 4 grid."),
            """
            ### Diagonals have a constant sum or difference

            On a diagonal that runs from top-right to bottom-left (an "anti-diagonal"), `r + c` is the same for every
            cell. On a diagonal running top-left to bottom-right, `r - c` is the same. So "visit diagonal `d`" just means
            "visit the cells with `r + c = d`". For a fixed `d`, the column is `c = d - r`, and the only thing left is
            working out which rows are valid: `c` must be between 0 and `n - 1`, which gives
            `max(0, d - n + 1) ≤ r ≤ min(m - 1, d)`. There are `m + n - 1` diagonals in total.

            ### Neighbours with direction arrays

            The four neighbours of `(r, c)` are up, down, left and right. Rather than writing four copies of the same
            check, list the steps once and loop over them:
            """,
            fig(Grid(NEIGH, st={(1, 1): "active", (0, 1): "mark", (2, 1): "mark", (1, 0): "mark", (1, 2): "mark"}),
                caption="Steps (dr, dc): (-1, 0), (+1, 0), (0, -1), (0, +1). Add the four diagonal steps too if the problem says 8 neighbours."),
            """
            Every neighbour has to pass the bounds check `0 ≤ nr < m and 0 ≤ nc < n` before you read it. Put that check
            first in the condition, so the read never happens for cells off the edge.

            ### Rings (layers)

            The outer border of a grid is ring 0, the border of what's left inside is ring 1, and so on. A cell's ring is
            its distance to the nearest edge: `min(r, c, m - 1 - r, n - 1 - c)`. A grid has `(min(m, n) + 1) // 2` rings.
            Spiral reading and in-place rotation both work ring by ring.
            """,
            fig(Grid(RING_IDX, label="5 × 5"), Grid(RING_IDX_46, label="4 × 6"),
                caption="Each cell labelled with its ring. The innermost ring of a non-square grid can be a single line."),
            """
            ### Transforms are index maps

            Flipping, transposing and rotating don't change any values. They only change where each value goes. So the
            way to think about any transform is: "the value at `(r, c)` moves to where?". For an `m × n` grid:
            """,
            table(
                ["transform", "(r, c) goes to", "result size"],
                ["transpose (flip over the main diagonal)", "`(c, r)`", "n × m"],
                ["mirror left–right", "`(r, n - 1 - c)`", "m × n"],
                ["flip upside down", "`(m - 1 - r, c)`", "m × n"],
                ["rotate 90° clockwise", "`(c, m - 1 - r)`", "n × m"],
                ["rotate 180°", "`(m - 1 - r, n - 1 - c)`", "m × n"],
            ),
            fig(Grid(T, label="original 2 × 3"), Grid(TR, label="transposed"), Grid(MIR, label="mirrored"), Grid(ROT, label="rotated 90° clockwise"),
                caption="Each transform is just a rule for where each value goes. Write the rule down and the loops follow from it."),
            """
            Writing the result into a new grid is easy once you know the map. Doing it **in place** is harder, because
            you'd overwrite values you still need. The usual tricks are to swap values in cycles of four (ring by ring),
            or to build a transform out of simpler ones that are each easy to do in place, like a transpose and a mirror.
            """,
        ]),
        ("template", "The template", [
            """
            Read a grid in zigzag order: diagonal by diagonal, starting at the top-left, alternating direction each time.
            Even diagonals go up and to the right, odd diagonals go down and to the left.
            """,
            code(
                "Zigzag diagonal order",
                ZIGZAG,
                [
                    ("size", "`m` rows and `n` columns, and the list we'll fill.",
                     {"c": "`k` is where the next value goes in `out`. The grid is flat: `(r, c)` is at `r * n + c`."}),
                    ("diag", "Diagonals are numbered by `d = r + c`, from 0 (the top-left cell) to `m + n - 2` (the "
                             "bottom-right one)."),
                    ("rows", "The rows that actually exist on diagonal `d`. `c = d - r` has to stay between 0 and `n - 1`, "
                             "which gives `r` from `max(0, d - n + 1)` to `min(m - 1, d)`."),
                    ("cells", "Collect the diagonal's values top to bottom.",
                     {"c": "Walk the diagonal's rows in the right direction straight away, without a temporary list."}),
                    ("flip", "Even diagonals are read bottom to top, so reverse them. That alternation is what makes the zigzag.",
                     {"c": "On even diagonals start from the bottom row (`hi`) and go up; on odd ones start from `lo` and go down."}),
                    ("out", "Append the diagonal to the answer."),
                    ("ret", "Every cell, each exactly once, in zigzag order."),
                ],
                ZIGZAG_RUN,
                "zigzag([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]); zigzag([[7], [8], [9]])",
            ),
            """
            Notice the single-column grid in the second run. Every diagonal has exactly one cell, so the zigzag is just
            top to bottom. Always try a single row and a single column; they're where the bounds formulas break if
            they're wrong.
            """,
        ]),
        ("trace", "Trace it by hand", [
            walk(zw),
        ]),
        ("examples", "More examples", [
            """
            ### Finding peaks with direction arrays

            A peak is a cell bigger than every neighbour above, below, left and right. Cells on the edge have fewer
            neighbours, and the missing ones just don't count against them.
            """,
            walk(pw),
            f"""
            ### Summing each ring

            In this 5 × 5 grid the rings hold different values. The ring of each cell is its distance to the nearest edge,
            so one pass over the grid can add every value to its ring's total, with no spiral walking at all:
            """,
            fig(Grid(RG5, label="values"), Grid(RING_IDX, label="ring of each cell"), Bars(RS, labels=["ring 0", "ring 1", "ring 2"], label="ring sums"),
                caption=f"Ring 0 has 16 ones, ring 1 has 8 twos, ring 2 is the single 9: {RS}."),
        ]),
        ("variations", "Variations", [
            """
            ### Neighbours with direction arrays

            The peak count from *More examples*. The direction arrays keep the neighbour logic in one place, and the
            bounds check comes before the read.
            """,
            code(
                "Count peaks (4 neighbours)",
                PEAKS,
                [
                    ("dirs", "The four steps: up, down, left, right. Add `(-1,-1), (-1,1), (1,-1), (1,1)` for eight neighbours."),
                    ("size", "Grid size, and the running count."),
                    ("cells", "Visit every cell, row by row."),
                    ("each", "Assume it's a peak until a neighbour proves otherwise, then try all four directions."),
                    ("step", "The neighbour's coordinates."),
                    ("inside", "Only neighbours inside the grid count. The bounds check comes first, so a cell off the edge "
                               "is never read. A neighbour that's equal or bigger means this cell isn't a peak."),
                    ("count", "Survived every neighbour: one more peak."),
                    ("ret", "The number of peaks."),
                ],
                PEAKS_RUN,
                "count_peaks([[1, 4, 2, 2], [3, 1, 5, 1], [2, 6, 1, 3]]); count_peaks([[5, 5], [5, 5]])",
            ),
            """
            The all-5s grid has no peaks, because a neighbour that's *equal* is enough to disqualify a cell. Whether
            "bigger" means strictly bigger is exactly the kind of detail you should check in the problem statement.

            ### Rings by formula

            Instead of walking the rings, work out each cell's ring and add it to the right total.
            """,
            code(
                "Sum of each ring",
                RINGS,
                [
                    ("size", "Grid size."),
                    ("count", "A grid has `(min(m, n) + 1) // 2` rings: a 5 × 5 grid has 3, a 2 × 3 grid has 1."),
                    ("cells", "Visit every cell once."),
                    ("ring", "The distance to the nearest edge: to the top is `r`, to the left `c`, to the bottom `m - 1 - r`, "
                             "to the right `n - 1 - c`. The smallest of the four is the ring."),
                    ("add", "Add the value to its ring's total."),
                    ("ret", "One total per ring, outermost first.",
                     {"c": "Returns the number of rings; the totals are in `sums`."}),
                ],
                RINGS_RUN,
                "ring_sums(5 × 5 grid with rings of 1s, 2s and a 9); ring_sums([[4, 0, 1], [2, 5, 3]])",
            ),
            """
            ### Spiral and other ring walks

            When you need to *visit* the rings in order (spiral reading, rotating in place), keep four boundaries: `top`,
            `bottom`, `left`, `right`. Walk one side, move that boundary inwards, and repeat until the boundaries cross.
            The part that trips people up is the last ring of a non-square grid, which can be a single row or a single
            column. Check those cases explicitly so you don't visit the same cells twice.

            ### Writing to a new grid vs in place

            If the result has a different shape (a transpose of a non-square grid, a rotation of `m × n` into `n × m`),
            you need a new grid anyway. If it's square and the problem asks for in place, think in terms of index maps
            and cycles: each value moves along a short cycle of positions, and you can move all of them with a single
            temporary variable.
            """,
        ]),
        ("complexity", "What it costs", [
            """
            Every traversal in this lesson visits each of the `m × n` cells a constant number of times, so they're all
            O(m × n) time. That's also the size of the input, so you can't do better if you need to look at every cell.

            Extra memory depends on the output. Reading into a list is O(m × n) for the answer. The neighbour check and
            the ring sums use O(1) and O(min(m, n)) extra. A transform into a new grid uses O(m × n); an in-place square
            transform uses O(1).
            """,
            table(
                ["Task", "Time", "Extra space"],
                ["Read in any fixed order", "O(m × n)", "O(1) besides the output"],
                ["Check every cell's neighbours", "O(m × n × directions)", "O(1)"],
                ["Transform into a new grid", "O(m × n)", "O(m × n)"],
                ["Transform a square grid in place", "O(n²)", "O(1)"],
            ),
        ]),
        ("languages", "In your language", [
            """
            ### Python

            `len(grid)` rows and `len(grid[0])` columns (check the grid isn't empty first). Make a new grid with
            `[[0] * n for _ in range(m)]`, never `[[0] * n] * m`, which makes `m` references to the *same* row, so changing
            one changes them all. `zip(*grid)` transposes in one line and gives tuples.

            ### Java

            `int[][]` is an array of arrays, and rows can technically have different lengths. `grid[0].length` is the
            column count. `new int[m][n]` starts at zeros. Cloning a 2D array with `clone()` only copies the outer array;
            the rows are still shared.

            ### C++

            `vector<vector<int>>` like Java. For speed, a single `vector<int>` of size `m * n` indexed `r * n + c` avoids
            one allocation per row. `min({a, b, c, d})` takes the minimum of several values at once.

            ### C

            Use one flat block (`malloc(m * n * sizeof(int))`) and index it `r * n + c`, as this lesson's code does.
            Fixed-size `int grid[3][4]` works too, but passing variable-sized 2D arrays between functions is awkward, so
            the flat layout is the usual choice.
            """,
        ]),
        ("pitfalls", "Pitfalls and edge cases", [
            """
            - Mixing up rows and columns. `m` is the number of rows (`len(grid)`), `n` is the number of columns
              (`len(grid[0])`). Swapping them only shows up on non-square grids, so always test one.
            - Reading before checking bounds. Check `0 ≤ nr < m and 0 ≤ nc < n` first, then read.
            - Single row, single column, single cell. Bounds formulas and spiral loops often break here.
            - Visiting a cell twice in a spiral when the last ring is a single row or column.
            - In-place transforms that overwrite values you still need. Use a temporary, or swap in cycles.
            - Python's `[[0] * n] * m` creating shared rows.
            - Empty grids. `grid[0]` fails if there are no rows.
            """,
        ]),
        ("check", "Check yourself", [
            quiz(
                ("How many diagonals (constant r + c) does a 3 × 5 grid have, and which cells are on diagonal 4?",
                 "3 + 5 - 1 = 7 diagonals. Diagonal 4 has r + c = 4 with 0 ≤ r ≤ 2 and 0 ≤ c ≤ 4: (0, 4), (1, 3), (2, 2)."),
                ("What ring is cell (1, 4) in a 4 × 6 grid?",
                 "min(1, 4, 4 - 1 - 1, 6 - 1 - 4) = min(1, 4, 2, 1) = 1."),
                ("Where does the value at (r, c) go when you rotate an m × n grid 90° clockwise?",
                 "To (c, m - 1 - r), in an n × m result. The first column, read bottom to top, becomes the first row."),
                ("In `count_peaks`, why does the bounds check come before `grid[nr][nc]`?",
                 "Because `and` stops at the first false part. If the neighbour is off the grid, the read never happens. In the other order you'd index out of range (or, in Python, a negative index would silently read the wrong row)."),
                ("You flatten an m × n grid row by row. Where is cell (r, c), and where is flat index i?",
                 "Cell (r, c) is at r × n + c. Flat index i is at row i // n, column i % n."),
            ),
        ]),
    ],
)
