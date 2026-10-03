"""Binary Search: searching sorted grids."""
import heapq

from sol import Grid, Row, Steps, Vars, approach, fig, problem, sol, table  # noqa: F401


def stair_walk(W, g, target, label=None):
    r, c = 0, len(g[0]) - 1
    seen = {}
    while r < len(g) and c >= 0:
        v = g[r][c]
        st = dict(seen)
        if v == target:
            st[(r, c)] = "answer"
            W.step(f"({r}, {c}) = {v}: found.", Grid(g, st=st, label=label), result="true")
            return True
        st[(r, c)] = "active"
        if v > target:
            W.step(f"({r}, {c}) = {v} > {target}: everything below it in column {c} is even bigger, so drop the column.", Grid(g, st=st, label=label))
            for rr in range(r, len(g)):
                seen[(rr, c)] = "dim"
            c -= 1
        else:
            W.step(f"({r}, {c}) = {v} < {target}: everything left of it in row {r} is even smaller, so drop the row.", Grid(g, st=st, label=label))
            for cc in range(0, c + 1):
                seen[(r, cc)] = "dim"
            r += 1
    W.step("Walked off the grid: not present.", Grid(g, st=seen, label=label), result="false")
    return False


@problem
def staircase_search():
    g = [[2, 5, 9, 14], [4, 7, 11, 18], [6, 10, 15, 21], [12, 16, 19, 25]]
    target = 10
    m, n = len(g), len(g[0])

    w1 = Steps("Check every cell.")
    for r in range(m):
        for c in range(n):
            if g[r][c] == target:
                w1.step(f"Cell ({r}, {c}) = {target}: found after {r * n + c + 1} checks.", Grid(g, st={(rr, cc): "dim" for rr in range(m) for cc in range(n) if rr * n + cc < r * n + c} | {(r, c): "answer"}), result="true")
                break
        else:
            w1.step(f"Row {r}: no {target}.", Grid(g, st={(r, cc): "dim" for cc in range(n)}))
            continue
        break

    w2 = Steps("Each row is sorted: binary-search every row.")
    import bisect
    for r in range(m):
        j = bisect.bisect_left(g[r], target)
        hit = j < n and g[r][j] == target
        w2.step(f"Row {r}: binary search → " + (f"found at column {j}." if hit else "not here."), Grid(g, st={(r, cc): ("answer" if hit and cc == j else "active") for cc in range(n)}))
        if hit:
            w2.steps[-1]["result"] = "true"
            break

    w3 = Steps("Start at the top-right corner. Each comparison removes a whole row or a whole column.")
    stair_walk(w3, g, target)

    sol(
        "staircase-search",
        summary="""
            Stand on the **top-right** cell. If it's bigger than the target, its whole column (everything below it is even
            bigger) can't contain the target: step left. If it's smaller, its whole row (everything to its left is
            smaller) is out: step down. Each step removes a row or a column, so the search takes at most m + n steps.
        """,
        question=[
            """
            Every row is sorted left to right and every column top to bottom. Return true if `target` is in the grid.

            - **Rows don't continue each other:** a row can start below the previous row's end, so the grid is *not* one
              long sorted list. (That's the difference from **Seat Map Lookup**.)
            - **Duplicates** are allowed (non-decreasing).
            - **Size:** up to 1000 × 1000 = 10⁶ cells.
            """
        ],
        think=[
            f"""
            Take this grid and target {target}.
            """,
            fig(Grid(g, st={(0, n - 1): "active"}), caption="Top-right corner: the largest in its row, the smallest in its column."),
            f"""
            The top-left corner is useless as a start: both moves (right, down) increase the value. But the **top-right**
            corner sits at a crossroads: moving left decreases, moving down increases. So one comparison decides a
            direction:

            - corner > target: the target can't be in this column (the rest of it is even larger): move left;
            - corner < target: the target can't be in this row (the rest of it is even smaller): move down.

            Each step eliminates a full row or column, so after at most m + n steps you either find the target or fall off
            the grid. (The bottom-left corner works the same way, mirrored.)
            """,
        ],
        approaches=[
            approach(
                "Check every cell",
                "brute",
                "O(m · n)",
                "O(1)",
                idea=["Compare every cell with the target."],
                walk=w1,
                build=["Loop over all cells; return true on a match.", "Return false."],
                code={
                    "python": """
                        class Solution:
                            def inWarehouse(self, grid: List[List[int]], target: int) -> bool:
                                return any(v == target for row in grid for v in row)  #@scan
                    """,
                    "java": """
                        class Solution {
                            public boolean inWarehouse(int[][] grid, int target) {
                                for (int[] row : grid) for (int v : row) if (v == target) return true;  //@scan
                                return false;  //@none
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool inWarehouse(vector<vector<int>>& grid, int target) {
                                for (auto& row : grid) for (int v : row) if (v == target) return true;  //@scan
                                return false;  //@none
                            }
                        };
                    """,
                    "c": """
                        bool inWarehouse(int** grid, int gridSize, int* gridColSize, int target) {
                            for (int r = 0; r < gridSize; r++)  //@scan
                                for (int c = 0; c < gridColSize[r]; c++) if (grid[r][c] == target) return true;  //@scan
                            return false;  //@none
                        }
                    """,
                },
                lines=[("scan", "Every cell is compared."), ("none", "No match anywhere.")],
                complexity=["**Time O(m · n):** 10⁶ cells. **Space O(1).**"],
                limits=["Ignores both orderings."],
            ),
            approach(
                "Binary-search each row",
                "better",
                "O(m log n)",
                "O(1)",
                idea=["Every row is sorted, so binary-search each row for the target."],
                walk=w2,
                build=["For each row, run a lower-bound search for the target.", "Return true if any row has it."],
                code={
                    "python": """
                        from bisect import bisect_left

                        class Solution:
                            def inWarehouse(self, grid: List[List[int]], target: int) -> bool:
                                for row in grid:  #@rows
                                    j = bisect_left(row, target)  #@search
                                    if j < len(row) and row[j] == target:  #@search
                                        return True  #@search
                                return False  #@none
                    """,
                    "java": """
                        class Solution {
                            public boolean inWarehouse(int[][] grid, int target) {
                                for (int[] row : grid) {  //@rows
                                    if (Arrays.binarySearch(row, target) >= 0) return true;  //@search
                                }
                                return false;  //@none
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool inWarehouse(vector<vector<int>>& grid, int target) {
                                for (auto& row : grid) {  //@rows
                                    if (binary_search(row.begin(), row.end(), target)) return true;  //@search
                                }
                                return false;  //@none
                            }
                        };
                    """,
                    "c": """
                        bool inWarehouse(int** grid, int gridSize, int* gridColSize, int target) {
                            for (int r = 0; r < gridSize; r++) {  //@rows
                                int lo = 0, hi = gridColSize[r] - 1;  //@search
                                while (lo <= hi) {  //@search
                                    int mid = lo + (hi - lo) / 2;  //@search
                                    if (grid[r][mid] == target) return true;  //@search
                                    if (grid[r][mid] < target) lo = mid + 1; else hi = mid - 1;  //@search
                                }  //@search
                            }
                            return false;  //@none
                        }
                    """,
                },
                lines=[("rows", "Each row on its own."), ("search", "Standard binary search within the sorted row."), ("none", "No row contains the target.")],
                complexity=["**Time O(m log n):** about 10⁴ steps for 1000 × 1000. **Space O(1).**"],
                limits=["Uses the row order but not the column order. Using both lets each comparison discard a whole row or column."],
            ),
            approach(
                "Staircase walk from the top-right",
                "best",
                "O(m + n)",
                "O(1)",
                idea=["Start at (0, n − 1). Equal → true. Bigger than target → move left (drop the column). Smaller → move down (drop the row). Off the grid → false."],
                walk=w3,
                build=["`r = 0`, `c = n − 1`.", "While inside: compare, then `c −= 1` or `r += 1`.", "Return false when you leave the grid."],
                code={
                    "python": """
                        class Solution:
                            def inWarehouse(self, grid: List[List[int]], target: int) -> bool:
                                r, c = 0, len(grid[0]) - 1  #@start
                                while r < len(grid) and c >= 0:  #@loop
                                    v = grid[r][c]  #@loop
                                    if v == target:  #@hit
                                        return True  #@hit
                                    if v > target:  #@left
                                        c -= 1  #@left
                                    else:  #@down
                                        r += 1  #@down
                                return False  #@none
                    """,
                    "java": """
                        class Solution {
                            public boolean inWarehouse(int[][] grid, int target) {
                                int r = 0, c = grid[0].length - 1;  //@start
                                while (r < grid.length && c >= 0) {  //@loop
                                    int v = grid[r][c];  //@loop
                                    if (v == target) return true;  //@hit
                                    if (v > target) c--;  //@left
                                    else r++;  //@down
                                }
                                return false;  //@none
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool inWarehouse(vector<vector<int>>& grid, int target) {
                                int r = 0, c = (int) grid[0].size() - 1;  //@start
                                while (r < (int) grid.size() && c >= 0) {  //@loop
                                    int v = grid[r][c];  //@loop
                                    if (v == target) return true;  //@hit
                                    if (v > target) c--;  //@left
                                    else r++;  //@down
                                }
                                return false;  //@none
                            }
                        };
                    """,
                    "c": """
                        bool inWarehouse(int** grid, int gridSize, int* gridColSize, int target) {
                            int r = 0, c = gridColSize[0] - 1;  //@start
                            while (r < gridSize && c >= 0) {  //@loop
                                int v = grid[r][c];  //@loop
                                if (v == target) return true;  //@hit
                                if (v > target) c--;  //@left
                                else r++;  //@down
                            }
                            return false;  //@none
                        }
                    """,
                },
                lines=[("start", "The top-right corner: smallest of its column, largest of its row."), ("loop", "Stay inside the grid."), ("hit", "Found."), ("left", "Too big: everything below in this column is at least as big, so the column is ruled out."), ("down", "Too small: everything to the left in this row is at most as big, so the row is ruled out."), ("none", "Every row or column was ruled out.")],
                complexity=["**Time O(m + n):** at most 2000 steps for 1000 × 1000. **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - In a grid sorted by rows **and** columns, start at a corner where one direction increases and the other
              decreases (top-right or bottom-left). Each comparison discards a row or a column: O(m + n).
            - If rows also continue each other, the grid is one sorted list and plain binary search gives O(log(m·n)).
            """
        ],
    )


@problem
def seat_map_lookup():
    g = [[2, 4, 7, 9], [12, 15, 18, 20], [23, 26, 31, 35]]
    target = 18
    m, n = len(g), len(g[0])
    flat = [v for row in g for v in row]

    w1 = Steps("Check every seat.")
    k = flat.index(target)
    w1.step(f"After {k + 1} checks: found at ({k // n}, {k % n}).", Grid(g, st={(q // n, q % n): "dim" for q in range(k)} | {(k // n, k % n): "answer"}), result="true")
    w1.steps.insert(0, {"text": "Scan row by row, left to right.", "panels": [Grid(g)]})

    w2 = Steps("Staircase from the top-right: bigger → move left, smaller → move down.")
    stair_walk(w2, g, target)

    w3 = Steps("Read the grid as one sorted list of m·n seats: index k is row k // n, column k % n. Binary-search k.")
    w3.step(f"Flattened: {flat}.", Row(flat, slots=True))
    lo, hi = 0, m * n - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        v = g[mid // n][mid % n]
        hit = v == target
        w3.step(f"lo={lo}, hi={hi}, mid={mid} → row {mid // n}, column {mid % n}: {v}" + (" = target." if hit else (" < target → right." if v < target else " > target → left.")), Row(flat, st={q: "dim" for q in range(len(flat)) if q < lo or q > hi} | {mid: "answer" if hit else "active"}, ptr={"lo": lo, "mid": mid, "hi": hi}, slots=True), Grid(g, st={(mid // n, mid % n): "answer" if hit else "active"}))
        if hit:
            w3.steps[-1]["result"] = "true"
            break
        if v < target:
            lo = mid + 1
        else:
            hi = mid - 1

    sol(
        "seat-map-lookup",
        summary="""
            Because each row starts after the previous row ends, reading the grid row by row gives **one sorted list** of
            m · n numbers. Binary-search that virtual list, translating an index k into row `k / n`, column `k % n`.
            O(log(m · n)), with no copying.
        """,
        question=[
            """
            Each row is sorted, and each row's first number is bigger than the previous row's last. Return true if
            `target` appears. Required: O(log(m · n)).

            - **The "rows continue each other" rule** is what makes the whole grid one sorted sequence.
            - **Required time O(log(m·n))**, so a row-by-row or staircase scan isn't enough.
            - **Size:** up to 300 × 300.
            """
        ],
        think=[
            f"""
            Take this grid and target {target}. Read it row by row: `{flat}`. That's sorted from start to end, because
            every row picks up where the previous one stopped.
            """,
            fig(Grid(g), Row(flat, slots=True), caption="Row by row, the grid is one sorted list."),
            f"""
            So binary search applies directly to positions 0 … m·n − 1. We never need to build that list: position k is
            row `k // n`, column `k % n` (n = {n} columns). For example, position 6 is row 1, column 2, which holds 18.
            """,
        ],
        approaches=[
            approach(
                "Check every seat",
                "brute",
                "O(m · n)",
                "O(1)",
                idea=["Compare every cell with the target."],
                walk=w1,
                build=["Loop over all cells; return true on a match.", "Return false."],
                code={
                    "python": """
                        class Solution:
                            def hasSeat(self, rows: List[List[int]], target: int) -> bool:
                                return any(v == target for row in rows for v in row)  #@scan
                    """,
                    "java": """
                        class Solution {
                            public boolean hasSeat(int[][] rows, int target) {
                                for (int[] row : rows) for (int v : row) if (v == target) return true;  //@scan
                                return false;  //@none
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool hasSeat(vector<vector<int>>& rows, int target) {
                                for (auto& row : rows) for (int v : row) if (v == target) return true;  //@scan
                                return false;  //@none
                            }
                        };
                    """,
                    "c": """
                        bool hasSeat(int** rows, int rowsSize, int* rowsColSize, int target) {
                            for (int r = 0; r < rowsSize; r++)  //@scan
                                for (int c = 0; c < rowsColSize[r]; c++) if (rows[r][c] == target) return true;  //@scan
                            return false;  //@none
                        }
                    """,
                },
                lines=[("scan", "Every seat."), ("none", "Not found.")],
                complexity=["**Time O(m · n).** **Space O(1).**"],
                limits=["Uses no ordering at all."],
            ),
            approach(
                "Staircase from the top-right",
                "better",
                "O(m + n)",
                "O(1)",
                idea=["The grid also satisfies the weaker \"rows and columns sorted\" property, so the staircase walk works: bigger → move left, smaller → move down."],
                walk=w2,
                build=["Start at (0, n − 1).", "Bigger → `c −= 1`; smaller → `r += 1`; equal → true.", "Leaving the grid → false."],
                code={
                    "python": """
                        class Solution:
                            def hasSeat(self, rows: List[List[int]], target: int) -> bool:
                                r, c = 0, len(rows[0]) - 1  #@start
                                while r < len(rows) and c >= 0:  #@walk
                                    if rows[r][c] == target:  #@walk
                                        return True  #@walk
                                    if rows[r][c] > target:  #@walk
                                        c -= 1  #@walk
                                    else:  #@walk
                                        r += 1  #@walk
                                return False  #@none
                    """,
                    "java": """
                        class Solution {
                            public boolean hasSeat(int[][] rows, int target) {
                                int r = 0, c = rows[0].length - 1;  //@start
                                while (r < rows.length && c >= 0) {  //@walk
                                    if (rows[r][c] == target) return true;  //@walk
                                    if (rows[r][c] > target) c--; else r++;  //@walk
                                }
                                return false;  //@none
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool hasSeat(vector<vector<int>>& rows, int target) {
                                int r = 0, c = (int) rows[0].size() - 1;  //@start
                                while (r < (int) rows.size() && c >= 0) {  //@walk
                                    if (rows[r][c] == target) return true;  //@walk
                                    if (rows[r][c] > target) c--; else r++;  //@walk
                                }
                                return false;  //@none
                            }
                        };
                    """,
                    "c": """
                        bool hasSeat(int** rows, int rowsSize, int* rowsColSize, int target) {
                            int r = 0, c = rowsColSize[0] - 1;  //@start
                            while (r < rowsSize && c >= 0) {  //@walk
                                if (rows[r][c] == target) return true;  //@walk
                                if (rows[r][c] > target) c--; else r++;  //@walk
                            }
                            return false;  //@none
                        }
                    """,
                },
                lines=[("start", "Top-right corner."), ("walk", "Each comparison rules out a column (too big) or a row (too small)."), ("none", "Fell off the grid: not present.")],
                complexity=["**Time O(m + n).** **Space O(1).**"],
                limits=["Doesn't use the stronger \"rows continue each other\" property, and O(m + n) misses the required O(log(m·n))."],
            ),
            approach(
                "Binary search on the flattened index",
                "best",
                "O(log(m · n))",
                "O(1)",
                idea=["Binary-search positions `[0, m·n − 1]`; the value at position k is `rows[k / n][k % n]`."],
                walk=w3,
                build=["`lo = 0`, `hi = m·n − 1`.", "Read `mid`'s value through `mid / n` and `mid % n`.", "Classic binary search."],
                code={
                    "python": """
                        class Solution:
                            def hasSeat(self, rows: List[List[int]], target: int) -> bool:
                                m, n = len(rows), len(rows[0])  #@dims
                                lo, hi = 0, m * n - 1  #@range
                                while lo <= hi:  #@loop
                                    mid = (lo + hi) // 2  #@loop
                                    v = rows[mid // n][mid % n]  #@map
                                    if v == target:  #@cmp
                                        return True  #@cmp
                                    if v < target:  #@cmp
                                        lo = mid + 1  #@cmp
                                    else:  #@cmp
                                        hi = mid - 1  #@cmp
                                return False  #@none
                    """,
                    "java": """
                        class Solution {
                            public boolean hasSeat(int[][] rows, int target) {
                                int m = rows.length, n = rows[0].length;  //@dims
                                int lo = 0, hi = m * n - 1;  //@range
                                while (lo <= hi) {  //@loop
                                    int mid = lo + (hi - lo) / 2;  //@loop
                                    int v = rows[mid / n][mid % n];  //@map
                                    if (v == target) return true;  //@cmp
                                    if (v < target) lo = mid + 1; else hi = mid - 1;  //@cmp
                                }
                                return false;  //@none
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            bool hasSeat(vector<vector<int>>& rows, int target) {
                                int m = rows.size(), n = rows[0].size();  //@dims
                                int lo = 0, hi = m * n - 1;  //@range
                                while (lo <= hi) {  //@loop
                                    int mid = lo + (hi - lo) / 2;  //@loop
                                    int v = rows[mid / n][mid % n];  //@map
                                    if (v == target) return true;  //@cmp
                                    if (v < target) lo = mid + 1; else hi = mid - 1;  //@cmp
                                }
                                return false;  //@none
                            }
                        };
                    """,
                    "c": """
                        bool hasSeat(int** rows, int rowsSize, int* rowsColSize, int target) {
                            int m = rowsSize, n = rowsColSize[0];  //@dims
                            int lo = 0, hi = m * n - 1;  //@range
                            while (lo <= hi) {  //@loop
                                int mid = lo + (hi - lo) / 2;  //@loop
                                int v = rows[mid / n][mid % n];  //@map
                                if (v == target) return true;  //@cmp
                                if (v < target) lo = mid + 1; else hi = mid - 1;  //@cmp
                            }
                            return false;  //@none
                        }
                    """,
                },
                lines=[("dims", "m rows of n seats."), ("range", "Positions of the virtual sorted list."), ("loop", "Classic binary search loop."), ("map", "Position → (row, column): `k / n` full rows come before it, and it's `k % n` seats into its row."), ("cmp", "Compare and halve."), ("none", "Not in the grid.")],
                complexity=["**Time O(log(m · n)):** about 17 steps for 300 × 300. **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - A grid whose rows continue each other is a sorted list in disguise: index k ↔ `(k / n, k % n)`.
            - Translate indices instead of copying data.
            - Compare with **Staircase Search**, where rows only satisfy the weaker property and O(m + n) is the best.
            """
        ],
    )


@problem
def kth_in_sorted_grid():
    g = [[1, 4, 7, 11], [2, 5, 8, 12], [3, 6, 9, 16], [10, 13, 14, 17]]
    k = 7
    n = len(g)
    flat = sorted(v for row in g for v in row)
    want = flat[k - 1]

    w1 = Steps("Collect all n² values, sort them, take the k-th.")
    w1.step(f"Copy all {n * n} values into one list: {[v for row in g for v in row]}.", Grid(g), Row([v for row in g for v in row], slots=True))
    w1.step(f"All values sorted: {flat}.", Grid(g), Row(flat, st={k - 1: "answer"}, slots=True), result=want)

    w2 = Steps("Keep the smallest unused value of every row in a min-heap. Pop k times; each pop pushes the next value of that row.")
    heap = [(g[r][0], r, 0) for r in range(n)]
    heapq.heapify(heap)
    used = set()
    w2.step("Heap starts with each row's first value.", Grid(g, st={(r, 0): "found" for r in range(n)}), Row(sorted(x[0] for x in heap), label="heap"))
    for t in range(1, k + 1):
        v, r, c = heapq.heappop(heap)
        used.add((r, c))
        if c + 1 < n:
            heapq.heappush(heap, (g[r][c + 1], r, c + 1))
        w2.step(f"Pop #{t}: {v} from row {r}" + (f"; push {g[r][c + 1]}." if c + 1 < n else "; that row is used up."), Grid(g, st={p: "dim" for p in used} | {(x[1], x[2]): "found" for x in heap} | {(r, c): ("answer" if t == k else "active")}), Row(sorted(x[0] for x in heap), label="heap"))
    w2.steps[-1]["result"] = str(want)

    def count_le(v):
        r, c, tot = n - 1, 0, 0
        while r >= 0 and c < n:
            if g[r][c] <= v:
                tot += r + 1
                c += 1
            else:
                r -= 1
        return tot

    w3 = Steps("Binary-search the value v. Count cells ≤ v with a staircase walk from the bottom-left. The answer is the smallest v with count ≥ k.")
    lo, hi = g[0][0], g[-1][-1]
    while lo < hi:
        mid = lo + (hi - lo) // 2
        cnt = count_le(mid)
        w3.step(f"v = {mid}: {cnt} cells ≤ {mid} → " + (f"≥ {k}: answer ≤ {mid}." if cnt >= k else f"< {k}: answer > {mid}."), Grid(g, st={(r, c): "found" for r in range(n) for c in range(n) if g[r][c] <= mid}), Vars(lo=lo, hi=hi, count=cnt))
        if cnt >= k:
            hi = mid
        else:
            lo = mid + 1
    w3.step(f"lo = hi = {lo}.", Grid(g, st={(r, c): "answer" for r in range(n) for c in range(n) if g[r][c] == lo}), result=lo)

    sol(
        "kth-in-sorted-grid",
        summary="""
            Rows and columns are sorted, so the number of cells ≤ v can be counted in O(n) by a staircase walk. That
            count only grows with v, so binary-search the smallest v whose count reaches k: O(n log(max − min)) time and
            O(1) memory. A min-heap over the rows is the natural middle ground: O(k log n) time, O(n) memory.
        """,
        question=[
            """
            An n × n grid has every row and every column sorted. Return the k-th smallest value, counting duplicates.

            - **Rows don't continue each other,** so the grid isn't one sorted list.
            - **Memory goal: less than O(n²)**, which rules out copying everything into one array.
            - **Values are ±10⁹:** the difference `hi − lo` can reach 2 × 10⁹, so compute the midpoint with 64-bit math or
              `lo + (hi − lo) / 2` in a wide type.
            """
        ],
        think=[
            f"""
            Take this 4 × 4 grid and k = {k}. Sorted, the values are `{flat}`; the {k}-th is {want}.
            """,
            fig(Grid(g, st={(r, c): "found" for r in range(n) for c in range(n) if g[r][c] <= want}), caption=f"The cells ≤ {want} form a staircase shape in the top-left."),
            f"""
            Notice the shape of "cells ≤ v": in each row it's a prefix, and the prefixes get shorter going down (columns
            are sorted). So you can count them with a staircase walk: start at the bottom-left; if the cell is ≤ v, the
            whole column above it is ≤ v too (add r + 1, move right); otherwise move up. That's O(n).

            With a cheap count, use the **binary search on the value** idea: the k-th smallest is the smallest v with at
            least k cells ≤ v. The search runs over the value range [{g[0][0]}, {g[-1][-1]}] (top-left to bottom-right).
            """,
        ],
        approaches=[
            approach(
                "Flatten and sort",
                "brute",
                "O(n² log n)",
                "O(n²)",
                idea=["Copy all n² values into one array, sort it, return index k − 1."],
                walk=w1,
                build=["Copy every value.", "Sort.", "Return element k − 1."],
                code={
                    "python": """
                        class Solution:
                            def kthInGrid(self, grid: List[List[int]], k: int) -> int:
                                return sorted(v for row in grid for v in row)[k - 1]  #@all
                    """,
                    "java": """
                        class Solution {
                            public int kthInGrid(int[][] grid, int k) {
                                int n = grid.length;
                                int[] all = new int[n * n];  //@all
                                for (int r = 0; r < n; r++) System.arraycopy(grid[r], 0, all, r * n, n);  //@all
                                Arrays.sort(all);  //@all
                                return all[k - 1];  //@all
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int kthInGrid(vector<vector<int>>& grid, int k) {
                                vector<int> all;  //@all
                                for (auto& row : grid) all.insert(all.end(), row.begin(), row.end());  //@all
                                sort(all.begin(), all.end());  //@all
                                return all[k - 1];  //@all
                            }
                        };
                    """,
                    "c": """
                        static int cmpInt(const void* a, const void* b) {  //@all
                            int p = *(const int*) a, q = *(const int*) b;  //@all
                            return (p > q) - (p < q);  //@all
                        }  //@all

                        int kthInGrid(int** grid, int gridSize, int* gridColSize, int k) {
                            int n = gridSize;
                            int* all = malloc(n * n * sizeof(int));  //@all
                            for (int r = 0; r < n; r++) memcpy(all + r * n, grid[r], n * sizeof(int));  //@all
                            qsort(all, n * n, sizeof(int), cmpInt);  //@all
                            int answer = all[k - 1];  //@all
                            free(all);  //@all
                            return answer;  //@all
                        }
                    """,
                },
                lines=[("all", "Every value in one array, sorted; the answer is at index k − 1.")],
                complexity=["**Time O(n² log n).** **Space O(n²)**, which the problem asks to avoid."],
                limits=["Ignores all the sorting already present and uses n² memory."],
            ),
            approach(
                "Min-heap over the rows",
                "better",
                "O(k log n)",
                "O(n)",
                idea=["Each row is sorted, so the overall next-smallest value is always the smallest among the rows' next unused values. Keep those n values in a min-heap; pop k times, each time pushing the popped row's next value."],
                walk=w2,
                build=["Push `(grid[r][0], r, 0)` for every row.", "Pop k times; after popping `(v, r, c)`, push `(grid[r][c + 1], r, c + 1)` if it exists.", "The k-th popped value is the answer."],
                code={
                    "python": """
                        import heapq

                        class Solution:
                            def kthInGrid(self, grid: List[List[int]], k: int) -> int:
                                n = len(grid)
                                heap = [(grid[r][0], r, 0) for r in range(n)]  #@init
                                heapq.heapify(heap)  #@init
                                for _ in range(k):  #@pop
                                    v, r, c = heapq.heappop(heap)  #@pop
                                    if c + 1 < n:  #@push
                                        heapq.heappush(heap, (grid[r][c + 1], r, c + 1))  #@push
                                return v  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int kthInGrid(int[][] grid, int k) {
                                int n = grid.length;
                                PriorityQueue<int[]> heap = new PriorityQueue<>((x, y) -> Integer.compare(x[0], y[0]));  //@init
                                for (int r = 0; r < n; r++) heap.add(new int[] {grid[r][0], r, 0});  //@init
                                int[] top = null;  //@pop
                                for (int t = 0; t < k; t++) {  //@pop
                                    top = heap.poll();  //@pop
                                    int r = top[1], c = top[2];  //@push
                                    if (c + 1 < n) heap.add(new int[] {grid[r][c + 1], r, c + 1});  //@push
                                }
                                return top[0];  //@ret
                            }
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int kthInGrid(vector<vector<int>>& grid, int k) {
                                int n = grid.size();
                                priority_queue<tuple<int, int, int>, vector<tuple<int, int, int>>, greater<>> heap;  //@init
                                for (int r = 0; r < n; r++) heap.push({grid[r][0], r, 0});  //@init
                                int v = 0;  //@pop
                                for (int t = 0; t < k; t++) {  //@pop
                                    auto [val, r, c] = heap.top();  //@pop
                                    heap.pop();  //@pop
                                    v = val;  //@pop
                                    if (c + 1 < n) heap.push({grid[r][c + 1], r, c + 1});  //@push
                                }
                                return v;  //@ret
                            }
                        };
                    """,
                    "c": """
                        typedef struct { int v, r, c; } Item;  //@heap

                        static void siftDown(Item* h, int size, int i) {  //@heap
                            while (1) {  //@heap
                                int l = 2 * i + 1, s = i;  //@heap
                                if (l < size && h[l].v < h[s].v) s = l;  //@heap
                                if (l + 1 < size && h[l + 1].v < h[s].v) s = l + 1;  //@heap
                                if (s == i) return;  //@heap
                                Item t = h[i]; h[i] = h[s]; h[s] = t;  //@heap
                                i = s;  //@heap
                            }  //@heap
                        }  //@heap

                        int kthInGrid(int** grid, int gridSize, int* gridColSize, int k) {
                            int n = gridSize, size = n;
                            Item* h = malloc(n * sizeof(Item));  //@init
                            for (int r = 0; r < n; r++) h[r] = (Item) {grid[r][0], r, 0};  //@init
                            for (int i = n / 2 - 1; i >= 0; i--) siftDown(h, size, i);  //@init
                            int v = 0;  //@pop
                            for (int t = 0; t < k; t++) {  //@pop
                                Item top = h[0];  //@pop
                                v = top.v;  //@pop
                                if (top.c + 1 < n) h[0] = (Item) {grid[top.r][top.c + 1], top.r, top.c + 1};  //@push
                                else h[0] = h[--size];  //@push
                                siftDown(h, size, 0);  //@push
                            }
                            free(h);  //@ret
                            return v;  //@ret
                        }
                    """,
                },
                lines=[
                    ("heap", "C has no heap: a binary min-heap ordered by value; `siftDown` restores the order after the top is replaced."),
                    ("init", "Every row's first (smallest) value goes in: n entries, each remembering its row and column.", {"c": "Build the heap bottom-up in O(n)."}),
                    ("pop", "The heap's top is the smallest value not yet taken anywhere in the grid."),
                    ("push", "Replace it with the next value of the same row (if any), so the heap again holds each row's next candidate.", {"c": "Overwrite the top with the row's next value (or the last heap item when the row is exhausted) and sift it down: one O(log n) step."}),
                    ("ret", "The k-th value popped."),
                ],
                complexity=["**Time O(k log n):** up to n² log n when k is large. **Space O(n)** for the heap."],
                limits=["The cost grows with k (up to n² pops). Counting cells ≤ v doesn't depend on k at all, so binary search on the value is faster for large k and needs no heap."],
            ),
            approach(
                "Binary search on the value with a staircase count",
                "best",
                "O(n log(max − min))",
                "O(1)",
                idea=["Search v in `[grid[0][0], grid[n−1][n−1]]`. `count(v)`: start at the bottom-left; if `grid[r][c] ≤ v`, add `r + 1` (the whole column above) and move right; else move up. If `count(mid) ≥ k`, `hi = mid`; else `lo = mid + 1`."],
                walk=w3,
                build=["`lo` = top-left, `hi` = bottom-right (the min and max).", "Midpoint with 64-bit arithmetic.", "Staircase count; move the bounds.", "Return `lo`."],
                code={
                    "python": """
                        class Solution:
                            def kthInGrid(self, grid: List[List[int]], k: int) -> int:
                                n = len(grid)
                                def count_at_most(v):  #@count
                                    r, c, total = n - 1, 0, 0  #@count
                                    while r >= 0 and c < n:  #@count
                                        if grid[r][c] <= v:  #@count
                                            total += r + 1  #@count
                                            c += 1  #@count
                                        else:  #@count
                                            r -= 1  #@count
                                    return total  #@count
                                lo, hi = grid[0][0], grid[-1][-1]  #@range
                                while lo < hi:  #@loop
                                    mid = (lo + hi) // 2  #@loop
                                    if count_at_most(mid) >= k:  #@move
                                        hi = mid  #@move
                                    else:  #@move
                                        lo = mid + 1  #@move
                                return lo  #@ret
                    """,
                    "java": """
                        class Solution {
                            public int kthInGrid(int[][] grid, int k) {
                                long lo = grid[0][0], hi = grid[grid.length - 1][grid.length - 1];  //@range
                                while (lo < hi) {  //@loop
                                    long mid = lo + (hi - lo) / 2;  //@loop
                                    if (countAtMost(grid, mid) >= k) hi = mid;  //@move
                                    else lo = mid + 1;  //@move
                                }
                                return (int) lo;  //@ret
                            }

                            private int countAtMost(int[][] grid, long v) {  //@count
                                int n = grid.length, r = n - 1, c = 0, total = 0;  //@count
                                while (r >= 0 && c < n) {  //@count
                                    if (grid[r][c] <= v) { total += r + 1; c++; }  //@count
                                    else r--;  //@count
                                }  //@count
                                return total;  //@count
                            }  //@count
                        }
                    """,
                    "cpp": """
                        class Solution {
                        public:
                            int kthInGrid(vector<vector<int>>& grid, int k) {
                                int n = grid.size();
                                auto countAtMost = [&](long long v) {  //@count
                                    int r = n - 1, c = 0, total = 0;  //@count
                                    while (r >= 0 && c < n) {  //@count
                                        if (grid[r][c] <= v) { total += r + 1; c++; }  //@count
                                        else r--;  //@count
                                    }  //@count
                                    return total;  //@count
                                };  //@count
                                long long lo = grid[0][0], hi = grid[n - 1][n - 1];  //@range
                                while (lo < hi) {  //@loop
                                    long long mid = lo + (hi - lo) / 2;  //@loop
                                    if (countAtMost(mid) >= k) hi = mid;  //@move
                                    else lo = mid + 1;  //@move
                                }
                                return (int) lo;  //@ret
                            }
                        };
                    """,
                    "c": """
                        static int countAtMost(int** grid, int n, long long v) {  //@count
                            int r = n - 1, c = 0, total = 0;  //@count
                            while (r >= 0 && c < n) {  //@count
                                if (grid[r][c] <= v) { total += r + 1; c++; }  //@count
                                else r--;  //@count
                            }  //@count
                            return total;  //@count
                        }  //@count

                        int kthInGrid(int** grid, int gridSize, int* gridColSize, int k) {
                            int n = gridSize;
                            long long lo = grid[0][0], hi = grid[n - 1][n - 1];  //@range
                            while (lo < hi) {  //@loop
                                long long mid = lo + (hi - lo) / 2;  //@loop
                                if (countAtMost(grid, n, mid) >= k) hi = mid;  //@move
                                else lo = mid + 1;  //@move
                            }
                            return (int) lo;  //@ret
                        }
                    """,
                },
                lines=[
                    ("count", "Cells ≤ v in O(n): from the bottom-left, a cell ≤ v means its whole column above it is ≤ v too (columns are sorted), so add r + 1 and move right; a cell > v means move up."),
                    ("range", "The answer lies between the smallest (top-left) and largest (bottom-right) value. Kept in 64 bits, since `hi − lo` can be 2 × 10⁹."),
                    ("loop", "Halve the value range."),
                    ("move", "At least k cells ≤ mid: the answer is ≤ mid. Otherwise above."),
                    ("ret", "The smallest v with ≥ k cells ≤ v, which is an actual grid value."),
                ],
                complexity=["**Time O(n log(max − min)):** about 32 counts of O(n) each. **Space O(1).**"],
            ),
        ],
        takeaways=[
            """
            - k-th smallest in a row- and column-sorted grid: **binary search on the value** + **staircase count**.
            - A min-heap merging sorted rows is the general "k-way merge"; it costs O(k log n).
            - Use 64-bit midpoints when the value range spans the whole 32-bit range.
            """
        ],
    )
